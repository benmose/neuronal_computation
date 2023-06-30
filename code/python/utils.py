import numpy as np
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