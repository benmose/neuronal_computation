import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


dir_path = os.path.dirname(os.path.realpath(__file__))
dat_dir_path = os.path.join(dir_path, "../../dat")

filename = os.path.join(dat_dir_path, "freq_diagram.dat")

x = []
y = []
t = []
lines = []

def shortest_distance(x1, y1, a, b, c):     
    d = (a * x1 + b * y1 + c) / (np.sqrt(a * a + b * b))
    return d


with open(filename, "r") as f:
    lines = f.readlines()

for line in lines:
    l = line.split(' ')
    if float(l[4]) == 8:
        tempd = shortest_distance(float(l[0]), 0.06, 0.91149071, -1, -0.01253742)
        x.append(tempd)
        y.append(float(l[1]))
 

def func(x,a,b, c):
    return a*np.sqrt(x+c) + b*(x+c)


dist = np.array(x)
f = np.array(y)


popt, pcov = curve_fit(func, dist, f)
print(popt)


plt.figure()
plt.plot(dist, f, 'o')
plt.plot(dist, func(dist, *popt))
plt.title(r'frequency to distance %1.5f*$\sqrt{x+%1.5f}$ + %1.5f*(x+%1.5f)'%
          (popt[0],
           popt[2],
           popt[1],
           popt[2]))
plt.legend(['original data', 'curve approximation'])
plt.xlabel('distance')
plt.ylabel('frequency')
plt.xlim(0, 1)
plt.ylim(0, 0.6)
plt.show()
#plt.savefig(os.path.join(root, 'f-dist_curve_approx.png'))
