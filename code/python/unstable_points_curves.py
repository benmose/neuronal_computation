import os
import numpy as np
from config import dat_dir_path
import matplotlib.pyplot as plt
from distance_utils import frequency_approx
from utils import read_coordinates_from_dat

dir_name = "stability"
dir_path = os.path.join(dat_dir_path, dir_name)

hbfilename = os.path.join(dir_path, "diluted_HB_diagram_iapp_1.dat")
lpfilename = os.path.join(dir_path, "diluted_LP_diagram_iapp_1.dat")
lpupperfilename = os.path.join(dir_path, 'diluted_upper_LP_diagram_iapp_1.dat')

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

