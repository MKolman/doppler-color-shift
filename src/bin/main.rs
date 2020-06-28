extern crate image;

use doppler_color_shift::convert::color_shift;

fn main() {
	let n = 10;
    for i in 0..=n {
		println!("Load {}", i);
    	let mut img = image::open("stoplight.jpg").unwrap().into_rgba();
    	// let mut img = image::open("stoplight.jpg").unwrap().into_rgba();
    	// let mut img = image::open("rainbow.png").unwrap().into_rgba();
		let velocity = (i-n/2) as f64 / n as f64/5.;
		println!("Start {}", i);
		color_shift(&mut img, velocity);
		println!("Saving {}", i);
		img.save(format!("result_{}.jpg", i)).unwrap();
    }
}
