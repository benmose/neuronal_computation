import os
import numpy as np
import matplotlib.pyplot as plt
from config import dat_dir_path
from utils import read_coordinates_from_dat, find_peaks_in_dat, find_signal_time_period

dir_name = "z_0_022_d_0_028"
dir_path = os.path.join(dat_dir_path, dir_name)

filename = os.path.join(dir_path, "test.dat")

x = []
y = []

x, y = read_coordinates_from_dat(filename, 0, 1)
z = np.array(x)
d = np.array(y)

r = find_peaks_in_dat(z,d)
t = find_signal_time_period(z,d)
print('Period: ', t, "Rate: ", 1/t, 1000/t)

plt.figure()
plt.plot(z, d)
plt.plot(z[r[2]], d[r[2]], 'x')
plt.show()

