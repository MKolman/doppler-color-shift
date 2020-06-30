use crate::xyz;

/// Get the value of the three LEDs we used to represent the screen.
/// The three colors they represent are roughly red green and blue.
pub fn get_led(lam: f64) -> xyz::Color {
	return xyz::Color::new(
		xyz::gauss(lam, 1., 650., 20., 20.),
		xyz::gauss(lam, 1., 550., 20., 20.),
		xyz::gauss(lam, 1., 450., 20., 20.),
	);
}

/// Same as `get_led` but as viewed while moving at `v` fraction of the
/// speed of light. The value can range `-1 < v < 1` and is equal to
/// `get_led` at `v = 0`.
pub fn get_shifted_led(lam: f64, v: f64) -> xyz::Color {
	let g = ((1.-v)/(1.+v)).sqrt();
	return get_led(lam * g);
}

/// Returns an integration matrix between the standard XYZ
/// color matching functions and the RGB functions described
/// by the function get_led.
///
/// We denote <AB> as an integral of A*B over all visible
/// wavelengths. so we can describe the result as:  
///
/// | <XR>, <XG>, <XB> |
/// | <YR>, <YG>, <YB> |
/// | <ZR>, <ZG>, <ZB> |
///
/// This matrix can be used to convert from LED defined color
/// space (R, G, B) to CIE XYZ format `M.RGB = XYZ`. M can be
/// inverted and used in the opposite direction.
pub fn get_integration_matrix(velocity: f64) -> xyz::Transformer {
	// Number of points of integration per nm
	let precision = 10;
	let fprecision = precision as f64;
	let mut result = xyz::Transformer::zeros();
	for lam in 350*precision..=800*precision {
		let flam = lam as f64/fprecision;
		let xyz = xyz::get_xyz(flam);
		let led = get_shifted_led(flam, velocity);
		for i in 0..3 {
			for j in 0..3 {
				result[(i,j)] += xyz[i]*led[j] / fprecision;
			}
		}
	}
	return result;
}

#[test]
fn test_stationary_matrix() {
	let want = xyz::Transformer::new(
		16.506741, 21.577936, 11.981054,
		6.929874, 42.592760, 2.410219,
		0.000077, 1.173931, 65.536597
	);
	let got = get_integration_matrix(0.);
	assert!((&got - &want).norm() < 1e-5, "Invalid stationary matrix {}", got);
}