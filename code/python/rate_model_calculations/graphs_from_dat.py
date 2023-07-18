import os
import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt


utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").joinpath("iapp_4").as_posix()
sys.path.append(utils_path)
sys.path.append(dat_path)

from utils import read_coordinates_from_dat

dir_name = "cycle"
bif_dir="stability"
# dir_name = "z_0_022_d_0_028"
dir_path = os.path.join(dat_path, dir_name)
bif_path=os.path.join(dat_path, bif_dir)

filename = os.path.join(dir_path, "diluted_z_0_1_d_0_1.dat")
ratefile = os.path.join(dir_path, "diluted_rate_z_0_1_d_0_1.dat")
lpfile = os.path.join(bif_path, "diluted_LP_z_0_06_d_0_01.dat")

x = []
y = []
rx = []
ry = []
t = []
lines = []

x, y = read_coordinates_from_dat(filename, 0, 1)
rx, ry = read_coordinates_from_dat(ratefile, 0, 1)
lx, ly = read_coordinates_from_dat(lpfile, 0, 1)


z = np.array(x)
d = np.array(y)
rz = np.array(rx)
rd = np.array(ry)
lz = np.array(lx)
ld = np.array(ly)


plt.figure()
plt.plot(z, d)
plt.plot(rz, rd)
plt.plot(lz, ld)

plt.title("rate and CB models")
plt.legend(['CB model', 'rate model'])
plt.xlabel('z')
plt.ylabel('d')


plt.xlim(0, 0.2)
plt.ylim(0, 0.2)
plt.show()
