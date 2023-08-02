import os
import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").as_posix()
sys.path.append(utils_path)
sys.path.append(dat_path)

from utils import read_coordinates_from_dat


class ComparisonFromData:
    def __init__(self, iapp_title, cycle_dir, cb_file_name, rate_file_name):
        dir_name = cycle_dir
        dir_path = os.path.join(dat_path, dir_name)

        self.filename = os.path.join(dir_path, cb_file_name)
        self.ratefile = os.path.join(dir_path, rate_file_name)
        self.iapp_str = iapp_title


    def plot_data(self, xmax = 0.3, ymax = 0.3):
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
        plt.plot(rz, rd)

        plt.title("rate and CB models for " + self.iapp_str)
        plt.legend(['CB model', 'rate model'])
        plt.xlabel('z')
        plt.ylabel('d')


        plt.xlim(0, xmax)
        plt.ylim(0, ymax)
        plt.show()

