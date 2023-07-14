import os
import numpy as np
from math import pow, dist
from scipy.optimize import minimize
from scipy.signal import find_peaks
from scipy.signal import peak_widths
from scipy.signal import argrelextrema




def read_coordinates_from_dat(filename: str, x_loc: int, y_loc: int) -> tuple:
    x=[]
    y=[]
    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        l = line.split(' ')
        x.append(float(l[x_loc]))
        y.append(float(l[y_loc]))

    return x,y

def leave_only_given_locations_in_file(filename: str, x_loc: int, y_loc: int, point_num: None):
    x = []
    y = []
    dirname = os.path.dirname(filename)
    file_name = "diluted_" + os.path.basename(filename)
    filepath = os.path.join(dirname, file_name)
    if point_num:
        x, y = read_coordinates_of_unstable_point_from_dat(filename, x_loc, y_loc, point_num)
    else:
        x, y = read_coordinates_from_dat(filename, x_loc, y_loc)
    with open(filepath, "w") as f:
        for i in range(len(x)):
            f.write(str(x[i]))
            f.write(' ')
            f.write(str(y[i]))
            f.write('\n')



def read_coordinates_of_unstable_point_from_dat(filename: str, x_loc: int, y_loc: int, point_num: float) -> tuple:
    x=[]
    y=[]
    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        l = line.split(' ')
        if float(l[4]) == point_num:
            x.append(float(l[x_loc]))
            y.append(float(l[y_loc]))
    return x,y   


def find_peaks_in_dat(x, y) -> tuple:
        sortId = np.argsort(x)
        tempx = x[sortId]
        tempy = y[sortId]

        # this way the x-axis corresponds to the index of x
        maxm = argrelextrema(tempy, np.greater)  # (array([1, 3, 6]),)
        minm = argrelextrema(tempy, np.less)  # (array([2, 5, 7]),)
        peaks, _ = find_peaks(tempy)
        return (tempx, tempy, peaks, maxm, minm)



def return_available_time_period(peaks_idx, time_array, pair_index):
    # if we have more than pair_index peaks than we at least have 2*pair_index
    #  elements in the array. we take the values from the pair_index pair
    i = pair_index*2
    while i > len(peaks_idx):
        i -= 2
    if i <= 0:
         return 0
    left_idx = int(peaks_idx[i-1])
    right_idx = int(peaks_idx[i-2])
    print(time_array[left_idx], time_array[right_idx])
    return time_array[left_idx] - time_array[right_idx]



def find_signal_time_period(x,y):
    p  = find_peaks_in_dat(x,y)
    return return_available_time_period(p[2], x, 3)


def shortes_distance_quadratic_func(x, y, coeff2, coeff1, coeff0):
    C0 = coeff0
    C1 = coeff1
    C2 = coeff2
    f = lambda x: C0 + C1 * x + C2 * pow(x, 2)

    # Define function to minimize
    p_x = x
    p_y = y
    min_f = lambda x: pow(x-p_x, 2) + pow(f(x) - p_y, 2)

    # Minimize
    min_res = minimize(min_f, 0)  # The starting point doesn't really matter here

    f_x = min_res.x[0]
    f_y = f(min_res.x[0])

    p = [p_x, p_y]
    q = [f_x, f_y]

    return dist(p, q)
