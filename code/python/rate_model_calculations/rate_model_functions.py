import numpy as np
import matplotlib.pyplot as plt

def l(x):
    return 0.91149071*x -0.01253742

#distance from above line
def dl(x1,y1):
    return -(0.91149071 * x1 -1 * y1 -0.01253742) / (np.sqrt((0.91149071 * 0.91149071) + 1))

def d_biff_iapp_1(x):
    return 0.972*(x**2)+0.69684*x-0.00627

def Freq_iapp_1(z,d):
    return 0.73515848*np.sqrt(d-d_biff_iapp_1(z))-0.30205245*(d-d_biff_iapp_1(z))

def M_iapp_1(z, d):
    if d>=d_biff_iapp_1(z):
        return (Freq_iapp_1(z,d))
    return (0)


def d_biff_iapp_2(x):
    return 1.40183*(x**2)+0.56385*x-0.00613

def Freq_iapp_2(z,d):
    return 0.73484029*np.sqrt(d-d_biff_iapp_1(z))-0.30128275*(d-d_biff_iapp_1(z))

def M_iapp_2(z, d):
    if d>=d_biff_iapp_2(z):
        return (Freq_iapp_1(z,d))
    return (0)

def d_biff_iapp_4(x):
    return 1.40057863*(x**2)+0.55638719*x-0.01718072

def Freq_iapp_2(z,d):
    return 0.73484029*np.sqrt(d-d_biff_iapp_1(z))-0.30128275*(d-d_biff_iapp_1(z))

def M_iapp_2(z, d):
    if d>=d_biff_iapp_2(z):
        return (Freq_iapp_1(z,d))
    return (0)


d = np.linspace(0, 1)

if True:
    plt.figure()
    plt.plot(d,Freq_iapp_1(0.07, d))
    plt.plot(d, Freq_iapp_2(0.07,d))
    plt.title('frequency vs d')

    plt.legend(['iapp = 1mA', 'iapp = 2ma'])

    plt.xlabel('d')
    plt.ylabel('frequency')
    plt.xlim(0, 1)
    plt.ylim(0, 0.6)
    plt.show()