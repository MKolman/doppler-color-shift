# Doppler Color Shift
A library to color shift images to see them as if you were moving at astronomical speeds towards/away from the image.

# Algorithm

1. Take a single sRGB pixel (sR, sG, sB).
2. Convert sRGB into standard CIE XYZ color space.
3. Convert XYZ into CIE RGB where components have well defined wavelength.
  * (R, G, B) -> (700nm, 546.1nm, 435.8nm)
4. Using doppler tranformation convert above wavelengths.
5. Construct a new color space using the transformed frequencies (dopRGB).
6. Convert dopRGB -> XYZ -> sRGB

```
function convert(image, velocity):
  dopRGB2XYZ := createDopRGB(velocity)
  for pixel in image:
  	sRGB := getColor(pixel)
    RGB := XYZ2RGB(sRGB2XYZ(sRGB))
    pixel.color = XYZ2sRGB(dopRGB2XYZ(RGB))
```

Using the Doppler formula convert 

# Sources
* [A Beginner’s Guide to (CIE) Colorimetry by Chandler Abraham on Medium](https://medium.com/hipster-color-science/a-beginners-guide-to-colorimetry-401f1830b65a)
