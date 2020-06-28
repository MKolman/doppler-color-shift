import numpy as np
from bisect import bisect
class CMF(object):
  @classmethod
  def load(cls, filename):    
    w, d = [], []
    with open(filename) as f:
      for line in f:
        l, *cmf = map(float, line.split(','))
        w.append(l)
        d.append(cmf)
    return CMF(w, d)

  def __init__(self, wavelength, data):
    self.wavelength = wavelength
    self.data = data
  def convert(self, matrix):
    return CMF(self.wavelength, [matrix@d for d in self.data])
  def at(self, lam):
    i = bisect(self.wavelength, lam)
    if i != 0 and abs(self.wavelength[i] - lam) > abs(self.wavelength[i-1] - lam):
      i -= 1
    return self.data[i]


def doppler(wavelengths, v):
  return np.sqrt((1-v)/(1+v))*wavelengths

XYZ2RGB = np.array([
  [0.4184700, -0.1586600, -0.082835],
  [-0.091169, 0.25243000, 0.0157080],
  [0.0009209, -0.0025498, 0.1786000],
]) / 0.17697
XYZ = CMF.load("data/lin2012xyz10e_fine_7sf.csv")
RGB = XYZ.convert(XYZ2RGB)

rgb = np.array([1., 1., 1.])
after = np.zeros(3)
normal_lam = np.array([650, 538.8, 435.8])
dop_lam = doppler(normal_lam, -0.1)
print(dop_lam)
for i, (l, dl, v) in enumerate(zip(normal_lam, dop_lam, rgb)):
  print(RGB.at(dl)/RGB.at(l)[i])
  after += RGB.at(dl)*v/RGB.at(l)[i]
print(after)

l = 434.8
for i in range(10):
  print(i, round(l, 2), RGB.at(l))
  l += 0.2
