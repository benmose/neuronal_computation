import os
import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
dat_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("dat").joinpath("iapp_2").as_posix()
sys.path.append(utils_path)
sys.path.append(dat_path)

from utils import shortes_distance_quadratic_func
from distance_utils import frequency2distance, frequency_approx


dir_name = "frequency"
dir_path = os.path.join(dat_path, dir_name)

func = lambda x,a,b,c: a*np.sqrt(x+c) + b*(x+c)

func1 = lambda x,a,b: a*np.sqrt(x) + b*(x)

rf = lambda x,a,b,c: a*np.sqrt(x) + b*x + c

ode_func = lambda x: -0.11013295*(x**2)+1.03349817*x+0.00310307

d, f, dist, popt, shift_const_d = frequency2distance("diluted_z_0_02_d_0_001.dat", dir_path, 0.02, func1)
d1, f1, dist1, popt1, shift_const_d1 = frequency2distance("diluted_z_0_05_d_0_01.dat", dir_path, 0.05, func1)
d2, f2, dist2, popt2, shift_const_d2 = frequency2distance("diluted_z_0_07_d_0_01.dat", dir_path, 0.07, func1)
shifted_d = d-shift_const_d
shifted_d1 = d1-shift_const_d1
shifted_d2 = d2-shift_const_d2

if False:
    x = np.array([0.02, 0.05, 0.07])
    y = np.array([shift_const_d, shift_const_d1, shift_const_d2])
    popta = frequency_approx(x, y, rf)
    print(popta)

    print("shifted: ", shift_const_d1)
    print("ode func: ", rf(0.05, *popta))
    print("dist of 0.01, 0: ", shortes_distance_quadratic_func(0.01, 0, *popta))


if True:
    popta = frequency_approx(shifted_d, f, func1)
    print(popta)

if False:
    plt.figure()
    plt.plot(d,f)
    plt.plot(d1, f1)
    plt.plot(d2, f2)
    plt.title('frequency vs d')

    plt.legend(['z=0.02', 'z=0.05', 'z=0.07'])

    plt.xlabel('d')
    plt.ylabel('frequency')
    plt.xlim(0, 1)
    plt.ylim(0, 0.6)
    plt.show()

if True:
    plt.figure()
    plt.plot(shifted_d,f)
    plt.plot(shifted_d1, f1)
    plt.plot(shifted_d2, f2)
    plt.plot(shifted_d, func1(shifted_d, *popta))



    s = (r'fit = %1.5f*$\sqrt{x}$ + %1.5f*(x)'% tuple(popta))

    plt.title(s)


    plt.legend(['z=0.02', 'z=0.05', 'z=0.07', 'fitted curve'])


    plt.xlabel('d')
    plt.ylabel('frequency')
    plt.xlim(0, 1)
    plt.ylim(0, 0.6)
    plt.show()

if False:
    plt.figure()
    plt.plot(d,f)
    plt.plot(d, func1(d, *popta))



    s = (r'shifted fit = %1.5f*$\sqrt{x}}$ + %1.5f*(x)'% tuple(popta))

    plt.title(s)


    plt.legend(['z=0.02', 'fitted curve'])


    plt.xlabel('d')
    plt.ylabel('frequency')
    plt.xlim(0, 1)
    plt.ylim(0, 0.6)
    plt.show()

    plt.figure()
    plt.plot(d1,f1)
    plt.plot(d1, func1(d1, *popta))



    s = (r'fit = %1.5f*$\sqrt{x}}$ + %1.5f*(x)'% tuple(popta))

    plt.title(s)


    plt.legend(['z=0.05', 'fitted curve'])


    plt.xlabel('d')
    plt.ylabel('frequency')
    plt.xlim(0, 1)
    plt.ylim(0, 0.6)
    plt.show()

    plt.figure()
    plt.plot(d2,f2)
    plt.plot(d2, func1(d2, *popta))



    s = (r'fit = %1.5f*$\sqrt{x}}$ + %1.5f*(x)'% tuple(popta))

    plt.title(s)


    plt.legend(['z=0.07', 'fitted curve'])


    plt.xlabel('d')
    plt.ylabel('frequency')
    plt.xlim(0, 1)
    plt.ylim(0, 0.6)
    plt.show()

if False:
    plt.figure()
    plt.plot(d1,f1)
    plt.plot(d1, func1(d1-0.03, *popta))

    print(popta)

    s = (r'fit = %1.5f*$\sqrt{x-0.03}}$ + %1.5f*(x-0.03)'% tuple(popta))

    plt.title(s)


    plt.legend(['z=0.05', 'fitted curve'])


    plt.xlabel('d')
    plt.ylabel('frequency')
    plt.xlim(0, 1)
    plt.ylim(0, 0.6)
    plt.show()

    plt.figure()
    plt.plot(d2,f2)
    plt.plot(d2, func1(d2-0.046, *popta))



    s = (r'fit = %1.5f*$\sqrt{x-0.05}}$ + %1.5f*(x-0.05)'% tuple(popta))

    plt.title(s)


    plt.legend(['z=0.07', 'fitted curve'])


    plt.xlabel('d')
    plt.ylabel('frequency')
    plt.xlim(0, 1)
    plt.ylim(0, 0.6)
    plt.show()