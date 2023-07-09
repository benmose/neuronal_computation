import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from config import dat_dir_path, media_dir_path
from utils import read_coordinates_from_dat

dir_name = "comparison"
dir_path = os.path.join(dat_dir_path, dir_name)

filename = os.path.join(dir_path, "slow_z_0_05_s_0_01.dat")
ratefile = os.path.join(dir_path, "rate_z_0_05_s_0_01.dat")
ratefile1 = os.path.join(dir_path, "rate_shift_0_01_z_0_05_s_0_01.dat")
ratefile2 = os.path.join(dir_path, "rate_shift_0_008_z_0_05_s_0_01.dat")

x = []
y = []
rx = []
ry = []
t = []
lines = []

x, y = read_coordinates_from_dat(filename, 4, 5)
rx, ry = read_coordinates_from_dat(ratefile, 1, 2)
rx1, ry1 = read_coordinates_from_dat(ratefile1, 1, 2)
rx2, ry2 = read_coordinates_from_dat(ratefile2, 1, 2)


z = np.array(x)
d = np.array(y)
rz = np.array(rx)
rd = np.array(ry)
rz1 = np.array(rx1)
rd1 = np.array(ry1)
rz2 = np.array(rx2)
rd2 = np.array(ry2)



plt.figure()
plt.plot(z, d)
plt.plot(rz, ry)
plt.plot(rz1, ry1)
plt.plot(rz2, ry2)

plt.title("rate and CB models")
plt.legend(['CB model', 'rate shift 0.02', 'rate shift 0.01', 'rate shift 0.008'])
plt.xlabel('z')
plt.ylabel('d')


plt.xlim(0, 0.125)
plt.ylim(0, 0.1)
plt.show()
