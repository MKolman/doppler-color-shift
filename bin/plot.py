import numpy as np
from matplotlib import pyplot as plt

lrgb2xyz = np.array([
    [0.4123865632529917,   0.35759149092062537, 0.18045049120356368],
    [0.21263682167732384,  0.7151829818412507,  0.07218019648142547],
    [0.019330620152483987, 0.11919716364020845, 0.9503725870054354]
])
xyz2lrgb = np.array([
    [ 3.2410032329763587,   -1.5373989694887855,  -0.4986158819963629],
    [-0.9692242522025166,    1.875929983695176,    0.041554226340084724],
    [ 0.055639419851975444, -0.20401120612390997,  1.0571489771875335]
  ])

def linear_from_srgb(value):
  if value <= 10.31475:
    return value / 3294.6
  else:
    return ((value + 14.025) / 269.025)**2.4

def srgb_from_linear(value):
  if value * 3294.6 < 10.:
    return value * 3294.6
  else:
    return 269.025 * value**(5.0 / 12.0) - 14.025

def xyz_from_srgb(srgb):
  return lrgb2xyz@[linear_from_srgb(v) for v in srgb]

def srgb_from_xyz(xyz):
  return np.array([srgb_from_linear(v) for v in xyz2lrgb@xyz])

def led_from_xyz():
  lams = np.linspace(300, 800, 1000)
  xyz = np.array(list(zip(*[get_xyz(l) for l in lams])))
  led = np.array(list(zip(*[get_led(l) for l in lams])))

  mat = np.array([[sum(l*x) for l in led] for x in xyz])
  return mat

def gauss(x, a, m, s1, s2):
  s = s1 if x < m  else s2
  return a * np.exp(-(x-m)**2/2./s**2)

def get_xyz(lam):
  configs = [
    [[1.056, 5998., 379., 310.], [0.362, 4420., 160., 267.], [-0.065, 5011., 204., 262.]],
    [[0.821, 5688., 469., 405.], [0.286, 5309., 163., 311.]],
    [[1.217, 4370., 118., 360.], [0.681, 4590., 260., 138.]],
  ]
  return np.array([sum(gauss(lam*10, *args) for args in x) for x in configs])

def get_led(lam):
  return np.array([
    gauss(lam, 1., 650., 20., 20.),
    gauss(lam, 1., 550., 20., 20.),
    gauss(lam, 1., 450., 20., 20.),
  ])

def clear():
  plt.cla()
  plt.clf()

def plot_xyz():
  clear()
  lams = np.linspace(380, 700, 200)
  xyz = np.array(list(zip(*[get_xyz(l) for l in lams])))
  colors = [[sum(x*y) for y in xyz] for x in xyz]
  print(colors)
  for x, c, l in zip(xyz, colors, "xyz"):
    c = np.array([srgb_from_linear(r) for r in xyz2lrgb@(c/max(c))])
    c /= max(c) * (1 + 0.5*(l=="y"))
    c = [max(r, 0) for r in c]
    print(c)
    plt.plot(lams, x, c=c, label="$\\widebar {}$".format(l))
  plt.legend()
  plt.grid(linestyle=":")
  plt.xlabel("Wavelength [nm]")
  plt.ylabel("XYZ color matching functions [1/nm]")
  plt.tight_layout()
  plt.savefig("../img/xyz_cmf.svg")

def plot_lrgb():
  clear()
  lams = np.linspace(380, 700, 200)
  xyz = np.array(list(zip(*[get_xyz(l) for l in lams])))
  lrgb = np.array(list(zip(*[xyz2lrgb@get_xyz(l) for l in lams])))
  colors = [[sum(x*r) for x in xyz] for r in lrgb]
  print(colors)
  for x, c, l in zip(lrgb, colors, "rgb"):
    c = np.array([srgb_from_linear(r) for r in xyz2lrgb@(c/max(c))])
    c /= max(c)
    c = [max(r, 0) for r in c]
    print(c)
    plt.plot(lams, x, c=c, label="$\\widebar {}$".format(l))
  plt.legend()
  plt.grid(linestyle=":")
  plt.xlabel("Wavelength [nm]")
  plt.ylabel("sRGB linear color matching functions [1/nm]")
  plt.tight_layout()
  plt.savefig("../img/lrgb_cmf.svg")

def plot_green():
  pass

def main():
  plot_xyz()
  plot_lrgb()
main()