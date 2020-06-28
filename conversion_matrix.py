import numpy as np

''' Convert colors from CIE RGB color space to XYZ
https://en.wikipedia.org/wiki/CIE_1931_color_space#Construction_of_the_CIE_XYZ_color_space_from_the_Wright%E2%80%93Guild_data
'''
RGB2XYZ = np.array([
  [2.768, 1.751, 1.130],
  [1.000, 4.590, 0.060],
  [0.000, 0.056, 5.594],
]) * 0.17697

''' Conver from XYZ color space to CIE RGB 
https://en.wikipedia.org/wiki/CIE_1931_color_space#Construction_of_the_CIE_XYZ_color_space_from_the_Wright%E2%80%93Guild_data
'''
XYZ2RGB = np.array([
  [0.4184700, -0.1586600, -0.082835],
  [-0.091169, 0.25243000, 0.0157080],
  [0.0009209, -0.0025498, 0.1786000],
]) / 0.17697


# Transformation matrix from XYZ to linear RGB
XYZ2lRGB = np.array([
  [3.2406, -1.5372, -0.4986],
  [-0.9689, 1.8758, 0.04150],
  [0.0557, -0.2040, 1.05700],
])

# Tranformation matrix from linear RGB to XYZ
lRGB2XYZ = np.array([
  [0.4124, 0.3576, 0.1805],
  [0.2126, 0.7152, 0.0722],
  [0.0193, 0.1192, 0.9505],
])
''' Transform from XYZ color space to sRGB as per 
https://en.wikipedia.org/wiki/SRGB#The_forward_transformation_(CIE_XYZ_to_sRGB)
'''
def lRGB2sRGB(lRGB):
  # A function to fix color values
  gamma = lambda u: 12.92 * u if u < 0.0031308 else 1.055*u**0.41666 - 0.055
  # Fix values
  sRGB = np.array([gamma(u) for u in lRGB])
  return sRGB

def sRGB2lRGB(sRGB):
  ''' Transform colors from sRGB color space to XYZ as per
  https://en.wikipedia.org/wiki/SRGB#The_reverse_transformation
  '''
  # Convert from sRGB to linear RGB
  gamma = lambda u: u/12.92 if u < 0.04045 else ((u+0.055)/1.055)**2.4
  lRGB = np.array([gamma(u) for u in sRGB])
  return lRGB

def makeDopRGB2XYZ(RGBCromaticity, whitepoint):
  print("RGB", RGBCromaticity)
  K = np.linalg.solve(RGBCromaticity.T, whitepoint)
  return (K[:, np.newaxis]*RGBCromaticity).T

if __name__ == '__main__':
  for i in range(3):
    v = [int(j==i) for j in range(3)]
    err = XYZ2RGB@RGB2XYZ@v - v
    assert err.dot(err) < 1e-6, err
    err = XYZ2lRGB@lRGB2XYZ@v - v
    assert err.dot(err) < 1e-6, err
    err = sRGB2lRGB(lRGB2sRGB(v)) - v
    assert err.dot(err) < 1e-6, err

  # print(np.array([
  #   [2.768, 1.751, 1.130],
  #   [1.000, 4.590, 0.060],
  #   [0.000, 0.056, 5.594],
  # ]) * 0.0041)

  xyz_cmf = np.array([
    [0.0114,  0.3741,  0.3343],
    [0.0041,  0.9841,  0.0180],
    [0.0000,  0.0123,  1.6561],
  ])

  ciergb_primaries = np.array([
    [0.7347,  0.2738, 0.1666],
    [0.2653,  0.7174, 0.0089],
    [0.0000,  0.0088, 0.8245],
  ])
  print(makeDopRGB2XYZ(ciergb_primaries.T, [1, 1, 1]))
  print(makeDopRGB2XYZ(xyz_cmf.T, [1, 1, 1]))