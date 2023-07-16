import os
import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").joinpath("iapp_2").as_posix()
sys.path.append(utils_path)
sys.path.append(dat_path)

from distance_utils import frequency_approx
from utils import read_coordinates_from_dat

dir_name = "stability"
dir_path = os.path.join(dat_path, dir_name)

hbfilename = os.path.join(dir_path, "diluted_HB_ic_z_0_06_d_0_01.dat")
lpfilename = os.path.join(dir_path, "diluted_LP_ic_z_0_06_d_0_01.dat")
lpupperfilename = os.path.join(dir_path, 'diluted_upper_LP_ic_z_0_06_d_0_01.dat')

func = lambda x,a,b,c: a*(x**2) + b*(x) + c

hx, hy = read_coordinates_from_dat(hbfilename, 0, 1)
lpx, lpy = read_coordinates_from_dat(lpfilename, 0, 1)
lplx, lply = read_coordinates_from_dat(lpupperfilename, 0, 1)
popt = frequency_approx(lplx, lply, func)

hz = np.array(hx)
hd = np.array(hy)
lpz = np.array(lpx)
lpd = np.array(lpy)
lplz = np.array(lplx)
lpld = np.array(lply)


plt.figure()
plt.plot(hz, hd)
plt.plot(lpz, lpd)
plt.plot(lplz, func(lplz, *popt))



s = (r'fit = %1.5f*$x^2$ + %1.5f*(x) +%1.5f'% tuple(popt))
print(popt)

plt.title(s)

plt.legend(['bifurcation', 'saddle', 'fitted curve'])

plt.xlabel('z')
plt.ylabel('d')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()

