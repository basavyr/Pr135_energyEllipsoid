import numpy as np

def GenerateSpins(I_0,I_max):
    spins=[]
    spins=np.arange(I_0,I_max,2.0)
    return spins

def SP_AngularComponents(j, theta):
    th=(theta*np.pi)/180.0
    j1=round(j*np.cos(th),4)
    j2=round(j*np.sin(th),4)
    SP_AM=[j1,j2]
    return SP_AM

def InertiaFactor(moi):
    A=1.0/(2.0*moi)
    return A

spinTable=GenerateSpins(5.5,25.5)

print(SP_AngularComponents(11/2,30))

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

spinValue=19/2
j=11/2
theta=30


print(AFunction(spinValue,20,40,j,theta))
print(uFunction(spinValue,20,40,10,j,theta))
print(v0Function(spinValue,20,40,j,theta))