import os
import numpy as np
import matplotlib.pyplot as plt
from config import dat_dir_path
from utils import read_coordinates_from_dat, find_peaks_in_dat, find_signal_time_period


dir_name = "z_0_02_d_0_02"
data_dir = "data"
dir_path = os.path.join(dat_dir_path, dir_name)
data_path = os.path.join(dat_dir_path, data_dir)

datafile = os.path.join(data_path, "dist.txt")
filename = os.path.join(dir_path, "fast.dat")

x = []
y = []

x, y = read_coordinates_from_dat(filename, 0, 1)
z = np.array(x)
d = np.array(y)

r = find_peaks_in_dat(z,d)
t = find_signal_time_period(z,d)

with open(datafile, "a") as f:
    f.write(r"%f, %f, %f" % (0.02, 0.02, t))
    f.write('\n')

print('Period: ', t, "Rate: ", 1/t, 1000/t)

plt.figure()
plt.plot(z, d)
plt.plot(z[r[2]], d[r[2]], 'x')
plt.show()

