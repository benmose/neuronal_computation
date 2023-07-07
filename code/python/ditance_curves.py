import os
import numpy as np
from config import dat_dir_path
import matplotlib.pyplot as plt
from distance_utils import frequency2distance, frequency_approx

dir_name = "frequency"
dir_path = os.path.join(dat_dir_path, dir_name)

func = lambda x,a,b,c: a*np.sqrt(x+c) + b*(x+c)

func1 = lambda x,a,b: a*np.sqrt(x) + b*(x)


d, f, dist, popt = frequency2distance("z_0_02_s_0_001.dat", dir_path, 0.02, func)
d1, f1, dist1, popt1 = frequency2distance("z_0_05_s_0_01.dat", dir_path, 0.05, func)
d2, f2, dist2, popt2 = frequency2distance("z_0_07_s_0_01.dat", dir_path, 0.07, func, 8)

shifted_d = d-0.00824477
shifted_d1 = d1-0.0298903
shifted_d2 = d2-0.0463035
popta = frequency_approx(shifted_d, f, func1)

plt.figure()
plt.plot(d,f)
plt.plot(d1, f1)
plt.plot(d2, f2)
plt.title('frequency vs d')

# s = (r'%1.5f*$\sqrt{x+%1.5f}$ + %1.5f*(x+%1.5f)'%
#           popt)

# s1 = (r'%1.5f*$\sqrt{x+%1.5f}$ + %1.5f*(x+%1.5f)'%
#           popt1)

plt.legend(['z=0.02', 'z=0.05', 'z=0.07'])

# plt.legend(['original data z=0.02',
#             s,
#             'original data z=0.05',
#             s1])
# plt.xlabel('distance')
plt.xlabel('d')
plt.ylabel('frequency')
plt.xlim(0, 1)
plt.ylim(0, 0.6)
plt.show()

plt.figure()
plt.plot(shifted_d,f)
plt.plot(shifted_d1, f1)
plt.plot(shifted_d2, f2)
plt.plot(shifted_d, func1(shifted_d, *popta))



s = (r'fit = %1.5f*$\sqrt{x}$ + %1.5f*(x)'% tuple(popta))

plt.title(s)

# s1 = (r'%1.5f*$\sqrt{x+%1.5f}$ + %1.5f*(x+%1.5f)'%
#           popt1)

plt.legend(['z=0.02', 'z=0.05', 'z=0.07', 'fitted curve'])

# plt.legend(['original data z=0.02',
#             s,
#             'original data z=0.05',
#             s1])
# plt.xlabel('distance')
plt.xlabel('d')
plt.ylabel('frequency')
plt.xlim(0, 1)
plt.ylim(0, 0.6)
plt.show()

