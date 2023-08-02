import os
import math
import numpy as np
from scipy.optimize import curve_fit
from utils import read_coordinates_from_dat, shortes_distance_quadratic_func

def frequency2distance(file_name, dir_path, dval, func): 
    filename = os.path.join(dir_path, file_name)
    basename = os.path.splitext(filename)[0]
    outfile = os.path.join(dir_path, basename + ".txt")

    dtmp, ftmp = read_coordinates_from_dat(filename, 0, 1)
    distmp = []

    C2, C1, C0 = (0.97248748,0.69684267,-0.00626603)

    #f = lambda x: C0 + C1 * x + C2 * pow(x, 2)
    

    with open(outfile, "w") as f:
        for i in range(len(dtmp)):
            disttemp = shortes_distance_quadratic_func(0.02, dtmp[i], C2, C1, C0)
            distmp.append(disttemp)
            f.write(r'%f, %f, %f' % (dval, dtmp[i], disttemp))
            f.write('\n')

    d = np.array(dtmp)
    f = np.array(ftmp)
    dist = np.array(distmp)

    popt , _ = curve_fit(func, dist, f)  
    return d, f, dist, popt, float(d[-1])


def frequency_approx(d, f, func):
    popt , _ = curve_fit(func, d, f)  
    return  popt

def frequency_approx_scaled_quad(d, f):
    tx = d*10**3
    ty = f*10**3
    func = lambda x,a,b,c: a*(x**2) + b*(x) + c
    popt , _ = curve_fit(func, tx, ty)  
    return  ([popt[0]*10**3, popt[1], popt[2]/10**3], func)


def dist(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def averaged_distance(set1x, set1y, set2x, set2y):
    points1 = list(zip(set1x, set1y))
    points2 = list(zip(set2x, set2y))
    
    min_len = min(len(points1), len(points2))
    distances = 0
    for i in range(min_len):
        distances += dist(points1[i], points2[i])
    avg_distance = distances / min_len
    return avg_distance
