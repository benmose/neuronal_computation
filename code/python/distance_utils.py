import os
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
