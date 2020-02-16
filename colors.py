import colour
def doppler(rgb, v=0):
  xyz = colour.sRGB_to_XYZ(rgb)
  sd = colour.XYZ_to_sd(xyz)
  print(sd)

doppler((1, 0, 0))