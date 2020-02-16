from matplotlib import pyplot as plt
import convert

def get_input(filename='data/stockman_and_sharpe_2000_linear_energy_01nm.csv'):
  with open(filename) as f:
    return zip(*[[float(x) if len(x) > 2 else None for x in line.split(',')] for line in f])

def get_XYZ_CMF():
  with open('data/XYZ_color_matching_functions.txt') as f:
    f.readline()
    lam, XYZ = [], []
    for line in f:
      line = line.split()
      lam.append(int(line[0]))
      XYZ.append(tuple(map(float, line[1:])))
    return lam, XYZ

def plot():
  lam, XYZ = get_XYZ_CMF()
  for x in zip(*XYZ):
    plt.plot(lam, x)
  plt.show()

def lim(val, lo=0, hi=1):
  return [min(hi, max(lo, v/sum(val))) for v in val]
def plot():
  lam, XYZ = get_XYZ_CMF()
  X, Y = [], []
  colors = []
  for xyz in XYZ[:-10]:
    X.append(xyz[0]/sum(xyz))
    Y.append(xyz[1]/sum(xyz))
    colors.append(lim(convert.XYZ_to_RGB(xyz)))
  print(colors)
  plt.scatter(X, Y, c=colors)
  plt.show()

plot()

def get_RGB_wavelength():
  ''' Returns R, G, B wavelength in nm
  Note: these are not sRGB primaries, but RGB
  ''' 
  return [700, 546.1, 435.8]

def sRGB_to_RGB(sRGB):
  return convert.XYZ_to_RGB(convert.sRGB_to_XYZ(sRGB))