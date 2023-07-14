import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from config import dat_dir_path, media_dir_path
from utils import read_coordinates_from_dat

if len(sys.argv) < 2:
    print("Wrong number of parameters!!!")
    print("Usage: ")
    print(sys.argv[0], " <filename> [title] [x label] [y label]")
    sys.exit(1)



filename = sys.argv[1]

x = []
y = []

x, y = read_coordinates_from_dat(filename, 0, 1)


z = np.array(x)
d = np.array(y)



plt.figure()
plt.plot(z, d)

if len(sys.argv) >= 3:
    plt.title(sys.argv[2])

if len(sys.argv) >= 4:
    plt.xlabel(sys.argv[3])

if len(sys.argv) >= 5:
    plt.ylabel(sys.argv[4])


plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()
