use nalgebra::{Vector3, Matrix3};

pub type Color = Vector3<f64>;
pub type Transformer = Matrix3<f64>;

/// A conversion matrix from linear sRGB color space into an XYZ space.
pub fn get_lrgb2xyz() -> Transformer {
	return Transformer::new(
		0.4123865632529917,   0.35759149092062537, 0.18045049120356368,
		0.21263682167732384,  0.7151829818412507,  0.07218019648142547,
		0.019330620152483987, 0.11919716364020845, 0.9503725870054354
	);
}
/// A conversion matrix from XYZ color space to a linear sRGB space
pub fn get_xyz2lrgb() -> Transformer {
	return Transformer::new(
		 3.2410032329763587,   -1.5373989694887855,  -0.4986158819963629,
		-0.9692242522025166,    1.875929983695176,    0.041554226340084724,
		 0.055639419851975444, -0.20401120612390997,  1.0571489771875335
	);
}

/// Returns a value of an asymmetrical Gaussian function
///
/// a exp((x-m)^2/-2s^2) where s = s1 is x < m else s2
///
/// # Arguments
///
/// * `x` - value at which to to evaluate
/// * `a` - scaling factor
/// * `m` - the middle of the gaussian function
/// * `s1` - function's width on the left side
/// * `s2` - function's width on the right side
pub fn gauss(x: f64, a: f64, m: f64, s1: f64, s2: f64) -> f64 {
	let s = if x < m { s1 } else { s2 };
	return a * (-(x-m).powi(2)/2./s.powi(2)).exp();
}

/// Returns X, Y, and Z color matching function values at
/// a given wavelength `lam` which is given in nanometers.
///
/// Typical values will be between 380 and 780
pub fn get_xyz(lam: f64) -> Color{
	let configs = [ // a, m, s1, s2 values for gauss
		vec![[1.056, 5998., 379., 310.], [0.362, 4420., 160., 267.], [-0.065, 5011., 204., 262.]],
		vec![[0.821, 5688., 469., 405.], [0.286, 5309., 163., 311.]],
		vec![[1.217, 4370., 118., 360.], [0.681, 4590., 260., 138.]],
	];
	let mut result: Color = Color::zeros();
	for x in 0..3 {
		for &[a, m, s1, s2] in &configs[x] {
			result[x] += gauss(lam*10., a/1.068, m, s1, s2);
		}
	}
	return result;
}

/// Performs an sRGB gamma expansion i.e. a number in [0, 255]
/// range, into a value in [0, 1] range.
pub fn linear_from_srgb(value: f64) -> f64 {
	if value <= 10.31475 {
		return value / 3294.6;
	} else {
		return ((value + 14.025) / 269.025).powf(2.4);
	}
}
/// Performs an sRGB gamma compression i.e. a number in [0, 1]
/// range, into a value in [0, 255] range.
pub fn srgb_from_linear(value: f64) -> f64 {
	if value * 3294.6 < 10. {
		return value * 3294.6;
	} else {
		return 269.025 * value.powf(5.0 / 12.0) - 14.025;
	}
}

/// Given an sRGB triplet of numbers in range [0, 255] it returns an
/// equivalent XYZ triplet in the range [0, 1]
pub fn xyz_from_srgb(srgb: &Color) -> Color {
	return get_lrgb2xyz() * srgb.map(linear_from_srgb);
}
/// Given an XYZ triplet of numbers in range [0, 1] it returns an
/// equivalent XYZ triplet in the range [0, 255].
pub fn srgb_from_xyz(xyz: &Color) -> Color {
	return (get_xyz2lrgb() * xyz).map(srgb_from_linear);
}

#[test]
fn test_gauss() {
	assert_eq!(gauss(0., 1., 0., 1., 2.), 1.);
	assert_eq!(gauss(0., 2., 0., 1., 2.), 2.);
	assert_eq!(gauss(2., 1., 0., 1., 2.), (-0.5_f64).exp());
	assert_eq!(gauss(-2., 1., 0., 1., 2.), (-2_f64).exp());
}

#[test]
fn test_get_xyz() {
	let d = 100;
	let df = d as f64;
	let mut integral = [0., 0., 0.];
	for lam in 380*d..=780*d {
		let tmp = get_xyz(lam as f64/df);
		for i in 0..3 {
			integral[i] += tmp[i]/df;
		}
	}
	// Make sure all three functions are normalized to 0.2%
	assert!((integral[0]-100.).abs() < 0.2, "{}", integral[0]);
	assert!((integral[1]-100.).abs() < 0.2, "{}", integral[1]);
	assert!((integral[2]-100.).abs() < 0.2, "{}", integral[2]);

	let xyz_ir = get_xyz(800.);
	for &x in &xyz_ir {
		assert!(x < 1e-5, "IR should be invisible but is instead {:?}", xyz_ir);
	}
	let xyz_uv = get_xyz(300.);
	for &x in &xyz_uv {
		assert!(x < 1e-5, "UV should be invisible but is instead {:?}", xyz_uv);
	}
	let xyz_b = get_xyz(450.);
	assert!(xyz_b[2] > 1., "Z={} is too small", xyz_b[2]);
	assert!(xyz_b[2] > xyz_b[0] && xyz_b[0] > xyz_b[1], "{:?} is not correct for 450nm", xyz_b);

	let xyz_g = get_xyz(550.);
	assert!(xyz_g[1] > 0.9, "Y={} is too small", xyz_g[1]);
	assert!(xyz_g[1] > xyz_g[0] && xyz_g[0] > xyz_g[2], "{:?} is not correct for 550nm", xyz_g);

	let xyz_r = get_xyz(600.);
	assert!(xyz_r[0] > 0.9, "X={} is too small", xyz_r[0]);
	assert!(xyz_r[0] > xyz_r[1] && xyz_r[1] > xyz_r[2], "{:?} is not correct for 600nm", xyz_r);
}

#[test]
fn test_linear_srgb() {
	let mut got: f64;
	for &x in &vec![0., 1., 50., 101., 123., 150., 255.] {
		got = linear_from_srgb(srgb_from_linear(x));
		assert!((got-x).abs() < 1e-10, "want {}, got {}", x, got);
		got = srgb_from_linear(linear_from_srgb(x));
		assert!((got-x).abs() < 1e-10, "want {}, got {}", x, got);
	}
	let c = Color::new(0., 1., 255.);
	let got = c.map(srgb_from_linear).map(linear_from_srgb);
	assert!((got - c).norm() < 1e-10, "want {}, got {}", c, got);
}
#[test]
fn test_srgb_xyz() {
	let mut got: Color;
	let mut want: Color;
	let rgb = Color::new(1., 150., 255.);
	let xyz = Color::new(1., 0.3, 0.01);

	want = Color::new(0.28962, 0.29035, 0.98666);
	got = xyz_from_srgb(&rgb);
	assert!((&want - &got).norm() < 1e-4, "want {}, got {}, diff: {}", want, got, (&want-&got).norm());

	want = Color::new(397.572, -1337.705, 15.576);
	got = srgb_from_xyz(&xyz);
	assert!((&want - &got).norm() < 1e-3, "want {}, got {}, diff: {}", want, got, (&want-&got).norm());

	got = srgb_from_xyz(&xyz_from_srgb(&rgb));
	assert!((&got-&rgb).norm() < 1e-10, "want {}, got {}", rgb, got);

	got = xyz_from_srgb(&srgb_from_xyz(&xyz));
	assert!((&got-&xyz).norm() < 1e-10, "want {}, got {}", xyz, got);
}