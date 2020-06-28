use crate::log;
use crate::led;
use crate::xyz;
use crate::xyz::{Color, Transformer};

use wasm_bindgen::prelude::*;
use wasm_bindgen::Clamped;
use web_sys::{CanvasRenderingContext2d, ImageData};

fn get_conversion_matrix(velocity: f64) -> Transformer {
	return xyz::get_xyz2lrgb() // XYZ -> lRGB
		* led::get_integration_matrix(velocity) // LED' -> XYZ
		* led::get_integration_matrix(0.).try_inverse().unwrap() // XYZ -> LED
		* xyz::get_lrgb2xyz(); // lRGB -> XYZ
}

pub fn color_shift_rgba_vec(vec:&mut Vec<u8>, velocity: f64) {
	let matrix = get_conversion_matrix(velocity);
	let mut linear_from_srgb_memo = [0f64; 256];
	for i in 0..256 { linear_from_srgb_memo[i] = xyz::linear_from_srgb(i as f64); }
	let mut rgb = Color::zeros();

	for j in (0..vec.len()).step_by(4) {
		for i in 0..3 {
			rgb[i] = linear_from_srgb_memo[vec[j+i] as usize];
		}
		for (i, c) in (matrix*rgb).iter().enumerate() {
			vec[j+i] = xyz::srgb_from_linear(*c).min(255.).max(0.).round() as u8;
		}
	}
}

pub fn color_shift(image: image::RgbaImage, velocity: f64) -> image::RgbaImage {
	let (w, h) = (image.width(), image.height());
	let mut vec = image.into_vec();
	color_shift_rgba_vec(&mut vec, velocity);
	return image::RgbaImage::from_vec(w, h, vec).unwrap()
}

#[wasm_bindgen]
pub fn color_shift_canvas(ctx: &CanvasRenderingContext2d, velocity: f64) -> Result<(), JsValue> {
	let canvas = ctx.canvas().unwrap();
	let (width, height) = (canvas.width(), canvas.height());
	let mut image_data = ctx.get_image_data(0., 0., width as f64, height as f64).unwrap().data().to_vec();
	color_shift_rgba_vec(&mut image_data, velocity);
	return ctx.put_image_data(&ImageData::new_with_u8_clamped_array_and_sh(Clamped(&mut image_data), width, height).unwrap(), 0., 0.);
}

// #[test]
// fn test_u8() {
// 	let mut f: f64;
// 	f = 1.;
// 	assert_eq!(f as u8, 1_u8);
// 	f = 100.8;
// 	assert_eq!(f as u8, 100_u8);
// 	f = 255.6;
// 	assert_eq!(f as u8, 255_u8);
// 	f = 355.6;
// 	assert_eq!(f as u8, 255_u8);
// 	f = -1.;
// 	assert_eq!(f as u8, 0_u8);
// }