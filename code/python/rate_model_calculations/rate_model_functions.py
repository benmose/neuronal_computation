import numpy as np

def l(x):
    return 0.91149071*x -0.01253742

#distance from above line
def dl(x1,y1):
    return -(0.91149071 * x1 -1 * y1 -0.01253742) / (np.sqrt((0.91149071 * 0.91149071) + 1))

def d_biff(x):
    return 0.972*(x**2)+0.69684*x-0.00627

def Freq(z,d):
    return 0.73515848*np.sqrt(d-d_biff(z))-0.30205245*(d-d_biff(z))

def M(z, d):
    if d>=d_biff(z):
        return (Freq(z,d))
    return (0)
