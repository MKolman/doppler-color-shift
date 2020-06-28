import numpy as np
import conversion_matrix as cm

def get_XYZ_CMF():
  with open('data/XYZ_color_matching_functions.txt') as f:
    f.readline()
    lam, XYZ = [], []
    for line in f:
      line = line.split()
      lam.append(int(line[0]))
      XYZ.append(tuple(map(float, line[1:])))
    return lam, XYZ

def get_XYZ_CMF2():
  with open('data/lin2012xyz2e_fine_7sf.csv') as f:
    f.readline()
    lam, XYZ = [], []
    for line in f:
      line = line.split(",")
      lam.append(float(line[0]))
      XYZ.append(tuple(map(float, line[1:])))
    return lam, XYZ

def get_wave_XYZ(lam):
  lams, cmf = get_XYZ_CMF2()
  if lam < lams[0] or lam > lams[-1]:
    return (0, 0, 0)
  d = (lams[1] - lams[0])/2
  for l, xyz in zip(lams, cmf):
    if abs(l-lam) <= d:
      return xyz

def get_dopRGB_primaries(v):
  lams = [700, 546.1, 435.8]
  delta = np.sqrt((1-v)/(1+v))
  lams = [delta*l for l in lams]
  print("lams", lams)
  return np.array([get_wave_XYZ(l) for l in lams])

def get_full_transform(v):
  dRGB2XYZ = cm.makeDopRGB2XYZ(get_dopRGB_primaries(v), [1, 1, 1])
  result = cm.XYZ2lRGB@dRGB2XYZ@cm.XYZ2RGB@cm.lRGB2XYZ
  return result

cm.RGB2XYZ = cm.makeDopRGB2XYZ(get_dopRGB_primaries(0), [1, 1, 1])
cm.XYZ2RGB = np.linalg.inv(cm.RGB2XYZ)
x = np.array([0, 100, 0])
for v in range(-10, 20):
  m = get_full_transform(v/100)
  print([max(min(int(round(i)), 255), 0) for i in m@x])