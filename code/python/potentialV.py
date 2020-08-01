#Testing the triaxial potential V(q) for different values of the parameter set
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp

def SP_AngularComponents(j, theta):
    th=(theta*np.pi)/180.0
    j1=round(j*np.cos(th),4)
    j2=round(j*np.sin(th),4)
    SP_AM=[j1,j2]
    return SP_AM

def InertiaFactor(moi):
    A=1.0/(2.0*moi)
    return A

def AFunction(I,I1,I2,j,theta):
    A1=InertiaFactor(I1)
    A2=InertiaFactor(I2)
    j2=SP_AngularComponents(j,theta)[1]
    T1=A2*(1-(j2/I))
    return T1-A1

def uFunction(I,I1,I2,I3,j,theta):
    A1=InertiaFactor(I1)
    A2=InertiaFactor(I2)
    A3=InertiaFactor(I3)
    T=(A3-A1)/AFunction(I,I1,I2,j,theta)
    return T

def v0Function(I,I1,I2,j,theta):
    A1=InertiaFactor(I1)
    j1=SP_AngularComponents(j,theta)[0]
    return (-1.0)*A1*j1/AFunction(I,I1,I2,j,theta)

def kFunction(I,I1,I2,I3,j,theta):
    return np.sqrt(uFunction(I,I1,I2,I3,j,theta))

def JacobiAmplitude(q,k):
    k2=np.power(k,2)
    JA=sp.ellipj(q,k2)
    return JA

def sn(q,k):
    return JacobiAmplitude(q,k)[0]

def cn(q,k):
    return JacobiAmplitude(q,k)[1]

def dn(q,k):
    return JacobiAmplitude(q,k)[2]

def JA(q,k):
    return JacobiAmplitude(q,k)[3]

def GenerateJAs(k): 
    qValues=np.arange(-8,8.1,0.5)
    potential=[]
    for q in qValues:
        V=JacobiAmplitude(q,k)[3]
        if(np.isnan(V)==False):
            potential.append(V)
    if(len(potential)==len(qValues)):
        return 'OK'
    return '!OK'

def Potential(q,I,I1,I2,I3,j,theta):
    k=kFunction(I,I1,I2,I3,j,theta)
    v0=v0Function(I,I1,I2,j,theta)
    t1=(I*(I+1)*np.power(k,2)+np.power(v0,2))
    s=sn(q,k)
    c=cn(q,k)
    d=dn(q,k)
    t2=(2.0*I+1)*v0*c*d
    V=t1*np.power(s,2)+t2
    return V

params=[9.5,91,11,59,5.5,-57]

qValues=np.arange(-8,8.1,0.2)
Vq=[]
for q in qValues:
    id_V=Potential(q,params[0],params[1],params[2],params[3],params[4],params[5])
    Vq.append(id_V)

plt.plot(qValues,Vq,'-r')
plt.savefig('potential.pdf',bbox_inches='tight')
plt.close()