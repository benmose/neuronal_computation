import os
import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").joinpath("iapp_4").as_posix()
sys.path.append(utils_path)
sys.path.append(dat_path)

from distance_utils import frequency_approx_scaled_quad
from utils import read_coordinates_from_dat

dir_name = "stability"
dir_path = os.path.join(dat_path, dir_name)

hbfilename = os.path.join(dir_path, "diluted_HB_z_0_06_d_0_01.dat")
lpfilename = os.path.join(dir_path, "diluted_LP_z_0_06_d_0_01.dat")
lpupperfilename = os.path.join(dir_path, 'diluted_LP_upper_z_0_06_d_0_01.dat')


hx, hy = read_coordinates_from_dat(hbfilename, 0, 1)
lpx, lpy = read_coordinates_from_dat(lpfilename, 0, 1)
lplx, lply = read_coordinates_from_dat(lpupperfilename, 0, 1)


hz = np.array(hx)
hd = np.array(hy)
lpz = np.array(lpx)
lpd = np.array(lpy)
lplz = np.array(lplx)
lpld = np.array(lply)


popt, func = frequency_approx_scaled_quad(lplz, lpld)

plt.figure()
plt.plot(hz, hd)
plt.plot(lplz, lpld)
plt.plot(lplz, func(lplz, *popt))
#plt.plot(tx, ty)
#plt.plot(tx, func(tx, *popt))



s = (r'fit = (%1.5f*$x^2$ + %1.5f*(x) +%1.5f)'% tuple(popt))
print(popt)

plt.title(s)

plt.legend(['bifurcation', 'saddle', 'fitted curve'])

plt.xlabel('z')
plt.ylabel('d')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()

