import os
import numpy as np
from speq import dl
import matplotlib.pyplot as plt
from config import dat_dir_path
from scipy.optimize import curve_fit



data_dir = "data"
data_path = os.path.join(dat_dir_path, data_dir)

datafile = os.path.join(data_path, "dist.txt")

lines = []
with open(datafile, 'r') as f:
    lines = f.readlines()

zl = []
ddl = []
fl = []
for line in lines:
    l = line.split(',')
    zl.append(float(l[0]))
    ddl.append(float(l[1]))
    fl.append(1/float(l[2]))

za = np.array(zl)
da = np.array(ddl)
fa = np.array(fl)

sortId = np.argsort(za)
z = za[sortId]
d = da[sortId]
f = fa[sortId]

dist = []
for i in range(len(z)):
    dst = dl(z[i], d[i])
    dist.append(dst)

def func(x,a,b):
    return a*np.sqrt(x) + b*x

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
plt.xlim(0, 0.2)
plt.ylim(0, 0.2)
plt.show()



