import numpy as np
import matplotlib.pyplot as plt


def SP_AngularComponents(j, theta):
    th = (theta*np.pi)/180.0
    j1 = round(j*np.cos(th), 4)
    j2 = round(j*np.sin(th), 4)
    SP_AM = [j1, j2]
    return SP_AM


def InertiaFactor(moi):
    A = 1.0/(2.0*moi)
    return A


def AFunction(I, I1, I2, j, theta):
    A1 = InertiaFactor(I1)
    A2 = InertiaFactor(I2)
    j2 = SP_AngularComponents(j, theta)[1]
    T1 = A2*(1-(j2/I))
    return T1-A1


def uFunction(I, I1, I2, I3, j, theta):
    A1 = InertiaFactor(I1)
    A2 = InertiaFactor(I2)
    A3 = InertiaFactor(I3)
    T = (A3-A1)/AFunction(I, I1, I2, j, theta)
    return T


def v0Function(I, I1, I2, j, theta):
    A1 = InertiaFactor(I1)
    j1 = SP_AngularComponents(j, theta)[0]
    return (-1.0)*A1*j1/AFunction(I, I1, I2, j, theta)


def kFunction(I, I1, I2, I3, j, theta):
    u = uFunction(I, I1, I2, I3, j, theta)
    if(u < 0.0):
        k = np.sqrt(abs(u))
        return k
    k = np.sqrt(u)
    return k


def A3C1(I, I1, I2, I3, j, theta, file):
    u = uFunction(I, I1, I2, I3, j, theta)
    A = AFunction(I, I1, I2, j, theta)
    k = kFunction(I, I1, I2, I3, j, theta)
    M = max(I1, I2, I3)
    if(u < 0.0 and u > -1.0 and A > 0 and k < 1.0 and (M == I1)):
        print(I1, I2, I3, A, u, k)
        # file.write(str(I1)+'  '+str(I2) + ' '+str(I3) + ' '+str(theta) +
        #            ' '+str(A)+' '+str(u)+' '+str(k)+'\n')
        file.write(str(I1)+'  '+str(I2) + ' '+str(I3) + ' '+str(theta)+'\n')


mois = np.arange(1.0, 121.0, 1.0)
thetas = np.arange(-180.0, 181.0, 1.0)

file = open('../../out/contourParams.dat', 'w')
for i1 in mois:
    for i2 in mois:
        for i3 in mois:
            for th in thetas:
                A3C1(9.5, i1, i2, i3, 6.5, th, file)

file.close()
