import os
import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").as_posix()
sys.path.append(utils_path)
sys.path.append(dat_path)

from distance_utils import frequency_approx_scaled_quad
from utils import read_coordinates_from_dat

class UnstablePointsCurve:
    def __init__(self, stability_dir, hb_file, LP_file, LP_upper_file):
        dir_name = stability_dir
        dir_path = os.path.join(dat_path, dir_name)

        hbfilename = os.path.join(dir_path, hb_file)
        lpfilename = os.path.join(dir_path, LP_file)
        lpupperfilename = os.path.join(dir_path, LP_upper_file)


        self.hx, self.hy = read_coordinates_from_dat(hbfilename, 0, 1)
        self.lpx, self.lpy = read_coordinates_from_dat(lpfilename, 0, 1)
        self.lplx, self.lply = read_coordinates_from_dat(lpupperfilename, 0, 1)


        self.hz = np.array(self.hx)
        self.hd = np.array(self.hy)
        self.lpz = np.array(self.lpx)
        self.lpd = np.array(self.lpy)
        self.lplz = np.array(self.lplx)
        self.lpld = np.array(self.lply)

    def plot_curves(self):
        popt, func = frequency_approx_scaled_quad(self.lplz, self.lpld)

        plt.figure()
        plt.plot(self.hz, self.hd)
        plt.plot(self.lplz, self.lpld)
        plt.plot(self.lplz, func(self.lplz, *popt))



        s = (r'fit = (%1.5f*$x^2$ + %1.5f*(x) +%1.5f)'% tuple(popt))
        print(popt)

        plt.title(s)

        plt.legend(['bifurcation', 'saddle', 'fitted curve'])

        plt.xlabel('z')
        plt.ylabel('d')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.show()

