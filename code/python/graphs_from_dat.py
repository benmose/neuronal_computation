import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from config import dat_dir_path, media_dir_path


filename = os.path.join(dat_dir_path, "full_test.dat")
figfile = os.path.join(media_dir_path, "LP_line_from_xppaut.png")
hbfile = os.path.join(dat_dir_path, "HB_diagram.dat")
lpfile = os.path.join(dat_dir_path, "LP_diagram.dat")
lpfilel = os.path.join(dat_dir_path, "LP_diagram_for_upper_line.dat")
ratefile = os.path.join(dat_dir_path, "rate_cycle.dat")

x = []
y = []
hbx = []
hby = []
lpx = []
lpy = []
lpxl = []
lpyl = []
rx = []
ry = []
t = []
lines = []

with open(filename, "r") as f:
    lines = f.readlines()

for line in lines:
    l = line.split(' ')
    x.append(float(l[4]))
    y.append(float(l[5]))
    # x.append(float(l[0]))
    # y.append(float(l[4]))

with open(hbfile, "r") as f:
    lines = f.readlines()

for line in lines:
    l = line.split(' ')
    if float(l[4]) == 8:
        hbx.append(float(l[0]))
        hby.append(float(l[1]))

 
with open(lpfile, "r") as f:
    lines = f.readlines()

for line in lines:
    l = line.split(' ')
    if float(l[4]) == 6:
        lpx.append(float(l[0]))
        lpy.append(float(l[1]))

with open(lpfilel, "r") as f:
    lines = f.readlines()

for line in lines:
    l = line.split(' ')
    if float(l[4]) == 6:
        lpxl.append(float(l[0]))
        lpyl.append(float(l[1]))

with open(ratefile, "r") as f:
    lines = f.readlines()

for line in lines:
    l = line.split(' ')
    rx.append(float(l[1]))
    ry.append(float(l[2]))
    # rx.append(float(l[0]))
    # ry.append(float(l[1]))


z = np.array(x)
d = np.array(y)
hbz = np.array(hbx)
hbd = np.array(hby)
lpz = np.array(lpx)
lpd = np.array(lpy)
lplz = np.array(lpxl)
lpld = np.array(lpyl)
rz = np.array(rx)
rd = np.array(ry)

def func(x,a,b):
    return a*x + b


z = np.array(x)
d = np.array(y)

popt, pcov = curve_fit(func, lplz, lpld)
print(popt)

plt.figure()
plt.plot(z, d)
plt.plot(rz, ry)
#plt.plot(hbz, hbd)
#plt.plot(lpz, lpd)

#plt.plot(lplz, lpld, 'o')

#plt.plot(lplz, func(lplz, *popt))
#plt.plot(lplz, func(lplz, 0.91149071, -0.007582))
#plt.title('HB, LP, zd cycle - Close Up')

plt.title("rate and CB models")
plt.legend(['CB model', 'rate model'])
#plt.legend(['zd cycle', 'zd rate', 'HB', 'LP', 'LP line'])
plt.xlabel('z')
plt.ylabel('d')

#plt.xlabel('t')
# plt.ylabel('z')

plt.xlim(0, 0.3)
plt.ylim(0, 0.25)
plt.show()
#plt.savefig(figfile)
