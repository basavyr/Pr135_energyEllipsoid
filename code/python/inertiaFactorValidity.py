import numpy as np
import matplotlib.pyplot as plt

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

def kFunction(I,I1,I2,I3,j,theta):
    k=np.sqrt(uFunction(I,I1,I2,I3,j,theta))
    return k

def ValidConditions(I,I1,I2,I3,j,theta):
    if(I1==I2 or I1==I3 or I2==I3):
        return 
    u=uFunction(I,I1,I2,I3,j,theta)
    uChiral=uFunction(I,I1,I2,I3,j,theta+180)
    # v0=v0Function(I,I1,I2,j,theta)
    # k=kFunction(I,I1,I2,I3,j,theta)
    A=AFunction(I,I1,I2,j,theta)
    AChiral=AFunction(I,I1,I2,j,theta+180)
    ok=0
    if(not np.isnan(u) and not np.isnan(A)):
        ok=1
    if(A>=0.0 and u<1.0 and u>0.0 and abs(u)<1.0):
        return 1
    return 0

spinValue=19/2
j=11/2
theta=30

thetas=np.arange(-180.0,180.5,10.0)
avalues=[]
avaluesChiral=[]
for th in thetas:
    avalues.append(AFunction(spinValue,90,100,5.5,th))
    avaluesChiral.append(AFunction(spinValue,90,100,5.5,th+180))

plt.plot(thetas,avalues,'-r')
plt.plot(thetas,avaluesChiral,'-b')
plt.savefig('potential.pdf',bbox_inches='tight')

mois=np.arange(1.0,120.5,10.0)

f=open('validParams.dat','w')

for i1 in mois:
    for i2 in mois:
        for i3 in mois:
            for th in thetas:
                if(ValidConditions(9.5,i1,i2,i3,5.5,th)):
                    # print(i1,i2,i3,th)
                    f.write(str(i1)+" "+str(i2)+" "+str(i3)+" "+str(th)+"\n")

f.close()
