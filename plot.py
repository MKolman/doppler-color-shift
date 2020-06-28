import numpy as np
from matplotlib import pyplot as plt
import convert
from random import randint

lam = np.linspace(350, 750, 200)
g = lambda m, s: lambda x: np.exp(-(x-m)**2/2/s**2)
plt.plot(lam, g(450, 20)(lam))
plt.plot(lam, g(550, 20)(lam))
plt.plot(lam, g(650, 20)(lam))
plt.show()
quit()
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

def get_RGB_CMF():
  lam, XYZ = get_XYZ_CMF()
  R, G, B = [], [], []
  for xyz in XYZ:
    r, g, b = convert.XYZ_to_RGB(xyz)
    R.append(r)
    G.append(g)
    B.append(b)
  return lam, np.array(R), np.array(G), np.array(B)

def save_rgb():
  with open('data/RGB_color_matching_functions.txt', 'w') as f:
    for lrgb in zip(*get_RGB_CMF()):
      f.write("{},\t{:.10f},\t{:.10f},\t{:.10f}\n".format(*lrgb))
def getMat():
  lam, *RGB = get_RGB_CMF()
  M = np.zeros(shape=(3, 3), dtype="double")
  for i, R in enumerate(RGB):
    for j, G in enumerate(RGB[:i+1]):
      M[i][j] = sum(r * g for r, g in zip(R, G))
      M[j][i] = M[i][j]
  return M
# print(getMat())
# quit()
def getRHS(values):
  _, *RGB = get_RGB_CMF()
  return [sum(v * r for v, r in zip(values, R)) for R in RGB]

def test():
  lam, R, G, B = get_RGB_CMF()
  M = getMat()
  N = np.array([
        [0.1648514774836012, -0.05534856790379279, 0.01928440056075473],
        [-0.05534856790379279, 0.3617779291905265, -0.03181723405477439],
        [0.01928440056075473, -0.03181723405477439, 0.2274085623041899]
         # 0.1648514774844627, -0.05534856790463882, 0.01928440056594918
         # -0.05534856790463882, 0.36177792919097296, -0.03181723405655824
         # 0.01928440056594918, -0.03181723405655823, 0.22740856230688897
      ])
  values = (R + G + B)
  rhs = getRHS(values)
  print(rhs)
  print(N@rhs)
  # for _ in range(100):
  #   r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
  #   values = (r*R + g*G + b*B)
  #   diff = [r, g, b] - np.linalg.solve(M, rhs) 
  #   diff2 = [r, g, b] - N@rhs 
  #   print(diff@diff, diff2@diff2)


# test()
# m = getMat()
# print()
# for line in np.linalg.inv(m):
#   print("{:.17f}, {:.17f}, {:.17f}".format(*line))
# save_rgb()
# quit()
def plot():
  lam, *XYZ = get_input()
  for x in XYZ:
    plt.plot(lam, x)
  plt.show()

def solve(RGB, spec):
  m = np.zeros((3, 3))
  v = np.zeros(3)
  for i in range(3):
    v[i] = sum(RGB[i]*spec)
    for j in range(3):
      m[i][j] = sum(RGB[i] * RGB[j])
  return np.linalg.solve(m, v)

def lim(val, lo=0, hi=1):
  return [min(hi, max(lo, v/sum(val))) for v in val]
def plot():
  lam, XYZ = get_XYZ_CMF()
  X, Y = [], []
  colors = []
  for xyz in XYZ:
    # X.append(xyz[0]/sum(xyz))
    # Y.append(xyz[1]/sum(xyz))
    colors.append(convert.XYZ_to_RGB(xyz))
  # plt.scatter(X, Y, c=colors)
  RGB = list(map(np.array, zip(*colors)))
  for i in range(3):
    RGB[i] /= max(RGB[i])
  for c in zip(RGB, "RGB", [650, 546, 436]):
    i = c[2] - lam[0]
    plt.plot(lam, c[0], c=c[1], label=c[1])
  W = RGB[0]+RGB[1]+RGB[2]
  for _ in range(20):
    for i, w in enumerate(W):
      W[i-1] = w if i >= 1 else 0
    K = solve(RGB, W)
    print(K)
  plt.plot(lam, W, c="k", label="W")
  plt.plot(lam, RGB[0]*K[0]+RGB[1]*K[1]+RGB[2]*K[2], "k:", label="W")
  for c, k, p in zip(RGB, K, "RGB"):
    plt.plot(lam, c*k, ":", c=p)
  plt.grid(linestyle=":")
  plt.legend()
  plt.xlabel("Wavelength [nm]")
  plt.ylabel("Color matching functions")
  plt.savefig("img/rgb_cmf2.svg")

plot()

def get_RGB_wavelength():
  ''' Returns R, G, B wavelength in nm
  Note: these are not sRGB primaries, but RGB
  ''' 
  return [700, 546.1, 435.8]

def sRGB_to_RGB(sRGB):
  return convert.XYZ_to_RGB(convert.sRGB_to_XYZ(sRGB))


print(sRGB_to_RGB((1, 0, 0)))
print(sRGB_to_RGB((0, 1, 0)))
print(sRGB_to_RGB((0, 0, 1)))
print(sRGB_to_RGB((1, 1, 1)))