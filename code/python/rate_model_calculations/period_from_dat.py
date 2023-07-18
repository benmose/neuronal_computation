import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pathlib


utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
sys.path.append(utils_path)
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").joinpath("iapp_1").as_posix()
sys.path.append(dat_path)

from utils import read_coordinates_from_dat, find_peaks_in_dat, find_signal_time_period


dir_name = "voltage"
dir_path = os.path.join(dat_path, dir_name)

filename = os.path.join(dir_path, "z_0_1_d_0_1.dat")

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

