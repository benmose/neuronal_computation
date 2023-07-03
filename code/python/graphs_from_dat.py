import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from config import dat_dir_path, media_dir_path
from utils import read_coordinates_from_dat

dir_name = "z_0_05_d_0_01"
# dir_name = "z_0_022_d_0_028"
dir_path = os.path.join(dat_dir_path, dir_name)

filename = os.path.join(dir_path, "full_test.dat")
ratefile = os.path.join(dir_path, "rate_cycle.dat")

x = []
y = []
rx = []
ry = []
t = []
lines = []

x, y = read_coordinates_from_dat(filename, 4, 5)
rx, ry = read_coordinates_from_dat(ratefile, 1, 2)


z = np.array(x)
d = np.array(y)
rz = np.array(rx)
rd = np.array(ry)



plt.figure()
plt.plot(z, d)
plt.plot(rz, ry)

plt.title("rate and CB models")
plt.legend(['CB model', 'rate model'])
plt.xlabel('z')
plt.ylabel('d')


plt.xlim(0, 0.125)
plt.ylim(0, 0.1)
plt.show()
