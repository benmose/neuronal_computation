import os
import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").as_posix()
sys.path.append(utils_path)
sys.path.append(dat_path)

from distance_utils import frequency_approx
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

    def plot_curves(self, maxx=0.2, maxy=0.2):
        func = lambda x,a,b,c,d: a*((x+d)**2) + b*(x+d) + c
        func1 = lambda x,a,b,c: a*((x)**2) + b*(x) + c
        popt = frequency_approx(self.lplz, self.lpld, func1)

        plt.figure()
        plt.plot(self.hz, self.hd)
        plt.plot(self.lplz, self.lpld)
        plt.plot(self.lplz, func1(self.lplz, *popt))



        s = (r'fit = (%1.5f*$(x)^2$ + %1.5f*(x) +%1.5f)'% tuple(popt))
        print(popt)
        print("max z: ", max(self.lplz))
        print("max d: ", max(self.lpld))

        plt.title(s)

        plt.legend(['bifurcation', 'saddle', 'fitted curve'])

        plt.xlabel('z')
        plt.ylabel('d')
        plt.xlim(0, maxx)
        plt.ylim(0, maxy)
        plt.show()

    def plot_curves_with_coeffs(self, maxx=0.2, maxy=0.2, coeffs = []):
        func = lambda x,a: coeffs[0]*((x+a)**2) + coeffs[1]*(x+a) + coeffs[0]
        func1 = lambda x,a,b,c: a*((x)**2) + b*(x) + c
        popt = frequency_approx(self.lplz, self.lpld, func)

        plt.figure()
        plt.plot(self.hz, self.hd)
        plt.plot(self.lplz, self.lpld)
        plt.plot(self.lplz, func(self.lplz, *popt))



        s = (r'fit = (%1.5f*$(x)^2$ + %1.5f*(x) +%1.5f)'% tuple(popt))
        print(popt)
        print("max z: ", max(self.lplz))
        print("max d: ", max(self.lpld))

        plt.title(s)

        plt.legend(['bifurcation', 'saddle', 'fitted curve'])

        plt.xlabel('z')
        plt.ylabel('d')
        plt.xlim(0, maxx)
        plt.ylim(0, maxy)
        plt.show()

