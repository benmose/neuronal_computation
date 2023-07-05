import os
import numpy as np
from config import dat_dir_path
import matplotlib.pyplot as plt
from distance_utils import frequency2distance

dir_name = "frequency"
dir_path = os.path.join(dat_dir_path, dir_name)

func = lambda x,a,b,c: a*np.sqrt(x+c) + b*(x+c)

dist, f, popt = frequency2distance("z_0_02_s_0_001.dat", dir_path, func)
dist1, f1, popt1 = frequency2distance("z_0_05_s_0_01.dat", dir_path, func)

plt.figure()
plt.plot(dist, f)
plt.plot(dist, func(dist, *popt))
plt.plot(dist1, f1)
plt.plot(dist1, func(dist1, *popt1))

plt.title('frequency vs distance')

s = (r'%1.5f*$\sqrt{x+%1.5f}$ + %1.5f*(x+%1.5f)'%
          (popt[0],
           popt[2],
           popt[1],
           popt[2]))

s1 = (r'%1.5f*$\sqrt{x+%1.5f}$ + %1.5f*(x+%1.5f)'%
          (popt1[0],
           popt1[2],
           popt1[1],
           popt1[2]))

plt.legend(['original data z=0.02',
            s,
            'original data z=0.05',
            s1])
plt.xlabel('distance')
plt.ylabel('frequency')
plt.xlim(0, 1)
plt.ylim(0, 0.6)
plt.show()

