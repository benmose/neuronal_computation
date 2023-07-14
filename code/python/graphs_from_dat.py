import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from config import dat_dir_path, media_dir_path
from utils import read_coordinates_from_dat

dir_name = "cycle"
bif_dir="stability"
# dir_name = "z_0_022_d_0_028"
dir_path = os.path.join(dat_dir_path, dir_name)
bif_path=os.path.join(dat_dir_path, bif_dir)

filename = os.path.join(dir_path, "diluted_init_cond_d_0_1_s_0_1.dat")
ratefile = os.path.join(dir_path, "diluted_init_cond_z_0_1_s_0_1_rate.dat")
lpfile = os.path.join(bif_path, "diluted_LP_diagram_iapp_1.dat")

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


plt.xlim(0, 0.5)
plt.ylim(0, 0.5)
plt.show()
