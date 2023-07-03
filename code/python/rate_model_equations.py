import numpy as np

def l(x):
    return 0.91149071*x -0.01253742

#distance from above line
def dl(x1,y1):
    return -(0.91149071 * x1 -1 * y1 -0.01253742) / (np.sqrt((0.91149071 * 0.91149071) + 1))
#dl(x1,y1)=-(0.91149071 * x1 -1 * y1 -0.007582) / (sqrt((0.91149071 * 0.91149071) + 1))

#Frequencey as a function of distance
def Freq(x): 
    return 0.88423543*np.sqrt(x + 0.04909662) -0.44740154*(x + 0.04909662)

#Points below the line has zero frequency.
def M(z, d):
    if(l(z)<d):
        dist = dl(z,d)
        print("in if: ", Freq(dist))
        return (Freq(dist))
    print("returning zero")
    return 0

def dinfavg(M):
    return 0.5*M


def zinfavg(M):
    return 0.9*M

print("Rate: ", M(0.022, 0.028))
