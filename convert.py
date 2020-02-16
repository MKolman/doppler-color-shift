import numpy as np
def RGB_to_XYZ(RGB):
  ''' Convert colors from CIE RGB color space to XYZ
  https://en.wikipedia.org/wiki/CIE_1931_color_space#Construction_of_the_CIE_XYZ_color_space_from_the_Wright%E2%80%93Guild_data
  '''
  M = np.array([
    [2.768, 1.751, 1.130],
    [1.000, 4.590, 0.060],
    [0.000, 0.056, 5.594],
  ])
  XYZ = M@RGB
  return XYZ

def XYZ_to_RGB(XYZ):
  ''' Conver from XYZ color space to CIE RGB 
  https://en.wikipedia.org/wiki/CIE_1931_color_space#Construction_of_the_CIE_XYZ_color_space_from_the_Wright%E2%80%93Guild_data
  '''
  M = np.array([
    [0.4184700, -0.1586600, -0.082835],
    [-0.091169, 0.25243000, 0.0157080],
    [0.0009209, -0.0025498, 0.1786000],
  ])
  RGB = M@XYZ
  return RGB

def XYZ_to_sRGB(XYZ):
  ''' Transform from XYZ color space to sRGB as per 
  https://en.wikipedia.org/wiki/SRGB#The_forward_transformation_(CIE_XYZ_to_sRGB)
  '''
  # Transformation matrix from XYZ to linear RGB
  M = np.array([
    [3.2406, -1.5372, -0.4986],
    [-0.9689, 1.8758, 0.04150],
    [0.0557, -0.2040, 1.05700],
  ])
  # Linear RGB
  lRGB = M@XYZ
  # A function to fix color values
  gamma = lambda u: 12.92 * u if u < 0.0031308 else 1.055*u**0.41666 - 0.055
  # Fix values
  sRGB = np.array([gamma(u) for u in lRGB])
  return sRGB

def normalize(arr):
  return np.array(arr)/sum(arr)

def sRGB_to_XYZ(sRGB):
  ''' Transform colors from sRGB color space to XYZ as per
  https://en.wikipedia.org/wiki/SRGB#The_reverse_transformation
  '''
  # Convert from sRGB to linear RGB
  gamma = lambda u: u/12.92 if u < 0.04045 else ((u+0.055)/1.055)**2.4
  lRGB = [gamma(u) for u in sRGB]
  # Tranformation matrix from linear RGB to XYZ
  M = np.array([
    [0.4124, 0.3576, 0.1805],
    [0.2126, 0.7152, 0.0722],
    [0.0193, 0.1192, 0.9505],
  ])
  XYZ = M@lRGB
  return XYZ

if __name__ == '__main__':
  print(normalize([2.768, 1, 0]))
  print(normalize([0.0114, 0.0041, 0]))
  for i in range(3):
    v = [int(j==i) for j in range(3)]
    err = XYZ_to_RGB(RGB_to_XYZ(v)) - v
    assert err.dot(err) < 1e-6, err
    err = XYZ_to_sRGB(sRGB_to_XYZ(v)) - v
    assert err.dot(err) < 1e-6, err

  print(np.array([
    [2.768, 1.751, 1.130],
    [1.000, 4.590, 0.060],
    [0.000, 0.056, 5.594],
  ]) * 0.0041)