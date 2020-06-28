use crate::led;
use crate::xyz;
use crate::xyz::Color;
use ndarray_linalg::solve::Inverse;

use wasm_bindgen::prelude::*;
use wasm_bindgen::Clamped;
use web_sys::{CanvasRenderingContext2d, ImageData};

fn get_conversion_matrix(velocity: f64) -> ndarray::Array2<f64> {
	return xyz::get_xyz2lrgb() // XYZ -> lRGB
		.dot(&led::get_integration_matrix(velocity)) // LED' -> XYZ
		.dot(&led::get_integration_matrix(0.).inv().unwrap()) // XYZ -> LED
		.dot(&xyz::get_lrgb2xyz()); // lRGB -> XYZ
}

pub fn color_shift(image: &mut image::RgbaImage, velocity: f64) {
	let matrix = get_conversion_matrix(velocity);
	let mut linear_from_srgb_memo = [0f64; 256];
	for i in 0..256 { linear_from_srgb_memo[i] = xyz::linear_from_srgb(&(i as f64)); }
	let mut rgb: Color = array![0., 0., 0.];
	for p in image.pixels_mut() {
		for i in 0..3 {
			rgb[i] = linear_from_srgb_memo[p[i] as usize];
		}
		for (i, c) in matrix.dot(&rgb).iter().enumerate() {
			p[i] = xyz::srgb_from_linear(&c).min(255.).max(0.).round() as u8;

		}
	}
}

#[wasm_bindgen]
pub fn color_shift_canvas(ctx: &CanvasRenderingContext2d, velocity: f64) -> Result<(), JsValue> {
	let canvas = ctx.canvas().unwrap();
	let (width, height) = (canvas.width(), canvas.height());
	let matrix = get_conversion_matrix(velocity);
	let mut linear_from_srgb_memo = [0f64; 256];
	for i in 0..256 { linear_from_srgb_memo[i] = xyz::linear_from_srgb(&(i as f64)); }
	let mut rgb: Color = array![0., 0., 0.];
	let mut image_data = ctx.get_image_data(0., 0., width as f64, height as f64).unwrap().data();
	for j in (0..(width*height) as usize).step_by(4) {
		for i in 0..3 {
			rgb[i] = linear_from_srgb_memo[image_data[j+i] as usize];
		}
		for (i, c) in matrix.dot(&rgb).iter().enumerate() {
			image_data[j+i] = xyz::srgb_from_linear(&c).min(255.).max(0.).round() as u8;

		}
	}
	return ctx.put_image_data(&ImageData::new_with_u8_clamped_array(Clamped(image_data.as_mut()), width).unwrap(), 0., 0.);
}

#[test]
fn test_u8() {
	let mut f: f64;
	f = 1.;
	assert_eq!(f as u8, 1_u8);
	f = 100.8;
	assert_eq!(f as u8, 100_u8);
	f = 255.6;
	assert_eq!(f as u8, 255_u8);
	f = 355.6;
	assert_eq!(f as u8, 255_u8);
	f = -1.;
	assert_eq!(f as u8, 0_u8);
}