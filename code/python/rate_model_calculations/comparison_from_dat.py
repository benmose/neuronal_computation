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


class ComparisonFromData:
    def __init__(self, cycle_dir, cb_file_name, rate_file_name):
        dir_name = cycle_dir
        dir_path = os.path.join(dat_path, dir_name)

        self.filename = os.path.join(dir_path, cb_file_name)
        self.ratefile = os.path.join(dir_path, rate_file_name)


    def plot_data(self):
        x = []
        y = []
        rx = []
        ry = []
        t = []
        lines = []

        x, y = read_coordinates_from_dat(self.filename, 0, 1)
        rx, ry = read_coordinates_from_dat(self.ratefile, 0, 1)


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

