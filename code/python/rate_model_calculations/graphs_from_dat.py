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

class GraphsFromDat:
    def __init__(self, title, cycle_dir, stability_dir, cb_file, rate_file, lp_file):
        self.title = title
        dir_name = cycle_dir
        bif_dir = stability_dir
        dir_path = os.path.join(dat_path, dir_name)
        bif_path=os.path.join(dat_path, bif_dir)

        filename = os.path.join(dir_path, cb_file)
        ratefile = os.path.join(dir_path, rate_file)
        lpfile = os.path.join(bif_path, lp_file)

        self.x = []
        self.y = []
        self.rx = []
        self.ry = []
        self.t = []
        self.lines = []

        self.x, self.y = read_coordinates_from_dat(filename, 0, 1)
        self.rx, self.ry = read_coordinates_from_dat(ratefile, 0, 1)
        self.lx, self.ly = read_coordinates_from_dat(lpfile, 0, 1)


        self.z = np.array(self.x)
        self.d = np.array(self.y)
        self.rz = np.array(self.rx)
        self.rd = np.array(self.ry)
        self.lz = np.array(self.lx)
        self.ld = np.array(self.ly)

    def plot_curves(self):
        plt.figure()
        plt.plot(self.z, self.d)
        plt.plot(self.rz, self.rd)
        plt.plot(self.lz, self.ld)
        #plt.plot(self.lz, d_biff_iapp_2(self.lz))

        plt.title("rate and CB models for " + self.title)
        plt.legend(['CB model', 'rate model', 'saddle line'])
        plt.xlabel('z')
        plt.ylabel('d')


        plt.xlim(0, 0.2)
        plt.ylim(0, 0.2)
        plt.show()


class MultipleGraphsFromDat:
    def __init__(self, title):
        self.x = []
        self.y = []
        self.legend = []
        self.title = title

    def add_file_to_plot(self, filename, legend):
        filepath = os.path.join(dat_path, filename)
        x, y = read_coordinates_from_dat(filepath, 0, 1)
        self.x.append(x)
        self.y.append(y)
        self.legend.append(legend)


    def plot(self, xmax=0.3, ymax=0.3):
        plt.figure()
        for i in range(len(self.x)):
            plt.plot(self.x[i], self.y[i])

        plt.title(self.title)
        plt.legend(self.legend)
        plt.xlabel('z')
        plt.ylabel('d')


        plt.xlim(0, xmax)
        plt.ylim(0, ymax)
        plt.show()
