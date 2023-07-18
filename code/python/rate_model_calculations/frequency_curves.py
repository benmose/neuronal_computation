import os
import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").as_posix()
sys.path.append(utils_path)
sys.path.append(dat_path)

from utils import shortes_distance_quadratic_func
from distance_utils import frequency2distance, frequency_approx

class FrequencyCurves:
    def __init__(self, frequency_dir):
        dir_name = frequency_dir
        self.dir_path = os.path.join(dat_path, dir_name)

        self.func = lambda x,a,b,c: a*np.sqrt(x+c) + b*(x+c)

        self.func1 = lambda x,a,b: a*np.sqrt(x) + b*(x)

        self.rf = lambda x,a,b,c: a*np.sqrt(x) + b*x + c

        self.zval = []
        self.d = []
        self.f = []
        self.dist = []
        self.popt = []
        self.shift_const_d = []


    def new_frequency_curve(self, file_name, z_val):
        d, f, dist, popt, shift_const_d = frequency2distance(file_name, 
                                                             self.dir_path, 
                                                             z_val, 
                                                             self.func1)
        self.zval.append(z_val)
        self.d.append(d)
        self.f.append(f)
        self.dist.append(dist)
        self.popt.append(popt)
        shifted_d = d-shift_const_d
        self.shift_const_d.append(shifted_d)


    def print_curve_coefficients(self):
        popta = frequency_approx(self.shift_const_d[0], self.f[0], self.func1)
        print(popta)


    def plot_curves(self):
        plt.figure()
        for i in range(len(self.d)):
            plt.plot(self.d[i], self.f[i])
        
        zval_str = map(lambda x: "z="+str(x), self.zval)
        plt.legend(list(zval_str))

        plt.xlabel('d')
        plt.ylabel('frequency')
        plt.xlim(0, 1)
        plt.ylim(0, 0.6)
        plt.show()

    def plot_shifted_curves(self):
        popta = frequency_approx(self.shift_const_d[0],
                                self.f[0],
                                self.func1)
        plt.figure()
        for i in range(len(self.shift_const_d)):
            plt.plot(self.shift_const_d[i],self.f[i])
        plt.plot(self.shift_const_d[0], self.func1(self.shift_const_d[0],
                                                    *popta))



        s = (r'fit = %1.5f*$\sqrt{x}$ + %1.5f*(x)'% tuple(self.popta))

        plt.title(s)

        zval_str = map(lambda x: "z="+str(x), self.zval)
        zval_str_list = list(zval_str)
        zval_str_list.append("fitted curve")

        plt.legend(zval_str_list)


        plt.xlabel('d')
        plt.ylabel('frequency')
        plt.xlim(0, 1)
        plt.ylim(0, 0.6)
        plt.show()

    def plot_fitted_curve(self, curve_number):
        popta = frequency_approx(self.shift_const_d[curve_number],
                        self.f[curve_number],
                        self.func1)

        plt.figure()
        plt.plot(self.d[curve_number], self.f[curve_number])
        plt.plot(self.d[curve_number], self.func1(self.d[curve_number], *popta))



        s = (r'shifted fit = %1.5f*$\sqrt{x}}$ + %1.5f*(x)'% tuple(popta))

        plt.title(s)


        plt.legend(['z='+str(self.zval[curve_number]), 'fitted curve'])


        plt.xlabel('d')
        plt.ylabel('frequency')
        plt.xlim(0, 1)
        plt.ylim(0, 0.6)
        plt.show()