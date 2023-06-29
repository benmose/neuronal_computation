import csv
import numpy as np

filename = "/Users/rammantzur/doctorate/thesis_research/rate_model/experiment_output/I3_5/21_06_23/full_test.dat"
ratefile = "/Users/rammantzur/doctorate/thesis_research/rate_model/experiment_output/I3_5/21_06_23/rate_test.dat"

x = [0.05]
y = [0.01]
rx = [0.05]
ry = [0.01]


with open(filename, "r") as f:
    lines = f.readlines()

for line in lines:
    l = line.split(' ')
    x.append(float(l[4]))
    y.append(float(l[5]))

with open(ratefile, "r") as f:
    lines = f.readlines()

for line in lines:
    l = line.split(' ')
    rx.append(float(l[1]))
    ry.append(float(l[2]))

# PARAMETERS
Iapp=1
gCad=1.0
#p taud=4.5
taud=100
#p taus=0.05
gKCa=1.0
#p mu=0.025,eps=0.005
mu=0.01
eps=0.012
THcm=-28.0
Kcm=-3.0
#p gCa=4.0
gm=3.5
gnap=0.04
gna=100.0
gkdr=20.0
gl=0.12
gh=0.05
Cm=1
Vna=55.0
Vk=-90
Vl=-70
Vh=-27.4
VCa=120
THm=-28.0
Km=-7.8
THh=-50.0
Kh=7.0
THn=-23.0
Kn=-15.0
THp=-53.0
Kp=-5.0
THz=-28.0
Kz=-3.0
#p tauz=83.0
tauz=400
THd=12.0
Kd=-12.0


def l(x):
    return 0.91149071*x -0.007582

def dl(x1,y1):
    return -(0.91149071 * x1 -1 * y1 -0.007582) / (np.sqrt((0.91149071 * 0.91149071) + 1))

def Freq(x):
    return 0.88423543*np.sqrt(x + 0.04909662) -0.44740154*(x + 0.04909662)

def M(z, d):
    if l(z)<d:
        return Freq(dl(z,d))
    else:
        return 0

def dinfavg(M):
    return 1.297*M

def zinfavg(M):
    return 0.9*M 


def Il(V):
    return gl*(V-Vl)

def Ina(V,h):
    return gna*(minf(V)**3)*h*(V-Vna)

def minf(V):
    return 1.0/(1.0+np.exp((V-THm)/Km))

def hinf(V):
    return 1.0/(1.0+np.exp((V-THh)/Kh))

def tauh(V):
    return 30.0/(np.exp((V+50.0)/15.0)+np.exp(-(V+50.0)/16.0))

def Ikdr(V,n):
    return gkdr*(n**4)*(V-Vk)

def ninf(V):
    return 1.0/(1.0+np.exp((V-THn)/Kn))

def taun(V):
    return 7.0/(np.exp((V+40.0)/40.0)+np.exp(-(V+40.0)/50.0))
#
def Inap(V):
    return gnap*pinf(V)*(V-Vna)

def pinf(V):
    return 1.0/(1+np.exp((V-THp)/Kp))
#
def Im(V,z):
    return gm*z*(V-Vk)

def zinf(V):
    return 1.0/(1+np.exp((V-THz)/Kz))

def ICad(V,d): 
    return gCad*d*(V-VCa)

def dinf(V):
    return 1.0/(1.0+np.exp((V-THd)/Kd))

#p Thr=-83.9,Kr=7.4
#
#
# INITIAL CONDITIONS
V0=-80.0
h0=0.0
n0=0.0
z0=0.05
d0=0.01
zinfint0=0.0
dinfint0=0.0
#
# FUNCTIONS
#
#Il(V)=gl*(V-Vl) 
#
# Ina(V,h)=gna*(minf(V)^3)*h*(V-Vna)
# minf(V)=1.0/(1.0+exp((V-THm)/Km))
# hinf(V)=1.0/(1.0+exp((V-THh)/Kh))
# tauh(V)=30.0/(exp((V+50.0)/15.0)+exp(-(V+50.0)/16.0))
#
# Ikdr(V,n)=gkdr*(n^4)*(V-Vk)
# ninf(V)=1.0/(1.0+exp((V-THn)/Kn))
# taun(V)=7.0/(exp((V+40.0)/40.0)+exp(-(V+40.0)/50.0))
# #
# Inap(V)=gnap*pinf(V)*(V-Vna)
# pinf(V)=1.0/(1+exp((V-THp)/Kp))
# #
# Im(V,z)=gm*z*(V-Vk)
# zinf(V)=1.0/(1+exp((V-THz)/Kz))
# #
#Ih(V,r)=gh*r*(V-Vh)
#rinf(V)=1.0/(1+exp((V-THr)/Kr))
#taur(V)=20.0+6000.0/(exp((V+140.0)/21.6)+exp(-(V+40.0)/22.7))
#
#mCainf(V)=1.0/(1.0+exp((V-THcm)/Kcm))
#ICa(V)=gCa*mCainf(V)*(V-VCa)
#zCa=Ca/(Ca+1)
#
#IKCa(V,z)=gKCa*zCa*(V-Vk)
#
# ICad(V,d)=gCad*d*(V-VCa)
# dinf(v)= 1.0/(1.0+exp((V-THd)/Kd))
#
# EQUATIONS
dt = 0.1
#above 3000 and we get overflow of the exp function.
steps = 3000

def V(V, h, n, z, d):
    return (-Il(V)-Ina(V,h)-Ikdr(V,n)-Inap(V)-Im(V,z)-ICad(V,d)+Iapp)/Cm
#V'=(-Il(V)-Ina(V,h)-Ikdr(V,n)-Inap(V)-IKCa(V,zCa)-ICas(V,s)+Iapp)/Cm
#V'=(-Ina(V,h)-Ikdr(V,n)-Im(V,z)-Inap(V)-Ih(V,r)-Il(V)+Iapp)/Cm
def h(V, h):
    return (hinf(V)-h)/tauh(V)

def n(V, n):
    return (ninf(V)-n)/taun(V)

def z(V, z):
    return (zinf(V)-z)/tauz

def d(V, d):
    return (dinf(V)-d)/taud

def zr(z, d):
    return (dinfavg(M(z,d))-z)/tauz

def dr(z, d):
    return (zinfavg(M(z,d))-d)/taud

def z_txt(V, z):
    return r'(%f-%f)/%f' % (zinf(V),z,tauz)

def d_txt(V, d):
    return r'(%f-%f)/%f' % (dinf(V),d,taud)

def zr_txt(z, d):
    return r'(%f-%f)/%f' % (dinfavg(M(z,d)), z, tauz)

def dr_txt(z, d):
    return r'(%f-%f)/%f' % (zinfavg(M(z,d)), d, taud)

t = [0]
V_t = [V0]
h_t = [h0]
n_t = [n0]
z_t = [z0]
d_t = [d0]
zr_t = [z0]
dr_t = [d0]
z_form = [str(z0)]
d_form = [str(d0)]
zr_form = [str(z0)]
dr_form = [str(d0)]



for i in range(steps):
    Vtemp = V(V_t[i], h_t[i], n_t[i], z_t[i], d0)*dt + V_t[i]
    htemp= h(V_t[i], h_t[i])*dt + h_t[i]
    ntemp = n(V_t[i], n_t[i])*dt + n_t[i]
    ztemp = z(V_t[i], z_t[i])*dt + z_t[i]
    dtemp = d(V_t[i], d_t[i])*dt + d_t[i]
    zrtemp = zr(zr_t[i], dr_t[i])*dt + zr_t[i]
    drtemp = dr(zr_t[i], dr_t[i])*dt + dr_t[i]
    zform = z_txt(V_t[i], z_t[i])
    dform = d_txt(V_t[i], d_t[i])
    zrform = zr_txt(zr_t[i], dr_t[i])
    drform = dr_txt(zr_t[i], dr_t[i])
    ttemp = t[i] + dt
    t.append(ttemp)
    V_t.append(Vtemp)
    h_t.append(htemp)
    n_t.append(ntemp)
    z_t.append(ztemp)
    d_t.append(dtemp)
    dr_t.append(drtemp)
    zr_t.append(zrtemp)
    z_form.append(zform)
    d_form.append(dform)
    zr_form.append(zrform)
    dr_form.append(drform)

ta = np.array(t)
za = np.array(z_t)
da = np.array(d_t)
zra = np.array(zr_t)
dra = np.array(dr_t)
zforma = np.array(z_form)
dforma = np.array(d_form)
zrforma = np.array(zr_form)
drforma = np.array(dr_form)
fza = np.array(x[:steps+1])
fda = np.array(y[:steps+1])
rza = np.array(rx[:steps+1])
rda = np.array(ry[:steps+1])

newfilePath = "/Users/rammantzur/doctorate/thesis_research/rate_model/experiment_output/I3_5/21_06_23/cb_rate_euler.csv"
# header = ['t', 'z cb', 'd cb', 'z rate', 'd rate', 'diff z', 'diff d', 'cb z formula', 'cb d form', 'rate z formula', 'rate d forumla']
# rows = zip(ta, za, da, zra, dra, za-zra, da-dra, z_form, d_form, zr_form, dr_form)
header = ['t', 'z cb model', 'cb model z dot right hand side','z rate model', 'rate model z dot right hand side', 'd cb model', 'cb model d dot right hand side','d rate model', 'rate model d dot right hand side', 'diff z', 'diff d']
rows = zip(ta, za, z_form, zra, zr_form, da, d_form, dra, dr_form, za-zra, da-dra)
with open(newfilePath, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)