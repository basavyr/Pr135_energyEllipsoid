import numpy as np
import matplotlib.pyplot as plt

import time


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


# the point A3 should be a minimum for negative values of u
def A3(I, I1, I2, I3, j, theta, file):
    if(I1 == I2 or I1 == I3 or I2 == I3):
        return
    u = uFunction(I, I1, I2, I3, j, theta)
    A = AFunction(I, I1, I2, j, theta)
    k = kFunction(I, I1, I2, I3, j, theta)
    M = max(I1, I2, I3)
    if(u < 0.0 and u > -1.0 and A > 0.0 and k < 1.0 and (M == I2)):
        print(I1, I2, I3, A, u, k)
        # file.write(str(I1)+'  '+str(I2) + ' '+str(I3) + ' '+str(theta) +
        #            ' '+str(A)+' '+str(u)+' '+str(k)+'\n')
        file.write(str(I1)+'  '+str(I2) + ' '+str(I3) + ' ' +
                   str(theta)+' | A='+str(A)+' u='+str(u)+' k='+str(k)+'\n')


# the point C1 should be a minimum for negative values of u


def C1(I, I1, I2, I3, j, theta, file):
    if(I1 == I2 or I1 == I3 or I2 == I3):
        return
    u = uFunction(I, I1, I2, I3, j, theta)
    A = AFunction(I, I1, I2, j, theta)
    k = kFunction(I, I1, I2, I3, j, theta)
    M = max(I1, I2, I3)

    # this condition will not provide any real and valid set of parameters (MOI,th)
    # if(u < 0.0 and u > -1.0 and A > 0.0 and k < 1.0 and (M == I1)):

    # this condition can provide a set of valid parameters, but ignoring positive A and subunitary k
    paramSetSize = 0

    #! implements RELAXED conditions
    #! C1_0 Only positive A's are considered => value of k can be anything
    #! C1_1 Only positive k's are considered subunitary=> value of A can be anything

    # ? C1_0
    if(u < 0.0 and u > -1.0 and A > 0.0 and (M == I1)):
        # print(I1, I2, I3, A, u, k)
        paramSetSize = paramSetSize+1
        # file.write(str(I1)+'  '+str(I2) + ' '+str(I3) + ' '+str(theta) +
        #            ' '+str(A)+' '+str(u)+' '+str(k)+'\n')
        file.write(str(I1)+'  '+str(I2) + ' '+str(I3) + ' ' +
                   str(theta)+' | A='+str(A)+' u='+str(u)+' k='+str(k)+'\n')

    # ? C1_1
    elif u < 0.0 and u > -1.0 and k < 1.0 and (M == I1):
        # print(I1, I2, I3, A, u, k)
        paramSetSize = paramSetSize+1
        # file.write(str(I1)+'  '+str(I2) + ' '+str(I3) + ' '+str(theta) +
        #            ' '+str(A)+' '+str(u)+' '+str(k)+'\n')
        file.write(str(I1)+'  '+str(I2) + ' '+str(I3) + ' ' +
                   str(theta)+' | A='+str(A)+' u='+str(u)+' k='+str(k)+'\n')
    return paramSetSize


mois = np.arange(1.0, 121.0, 5.0)
thetas = np.arange(-180.0, 181.0, 5.0)

# for i1 in mois:
#     for i2 in mois:
#         for i3 in mois:
#             for th in thetas:
#                 # A3C1(9.5, i1, i2, i3, 6.5, th, file)


class FindContourParams:
    def __init__(self, moi):
        self.moi = moi
    mois = np.arange(1, 121, 5.0)
    thetas = np.arange(-180, 180, 5.0)
    spin0 = 9.5
    j = 5.5

    def ShowMOI(self):
        return self.moi

    def FindParams(self):
        if(self.moi == 1):
            file = open('../../out/contourParams.dat', 'w')
            print('Find 1-axis quantization')
            totalSizeParams = 0
            for i1 in self.mois:
                for i2 in self.mois:
                    for i3 in self.mois:
                        for theta in self.thetas:
                            c = C1(self.spin0, i1, i2, i3, self.j, theta, file)
                            if(c == 1):
                                totalSizeParams = totalSizeParams+1
            print(
                f'The search found {totalSizeParams} total parameter sets...')
            file.write('The search found '+str(totalSizeParams) +
                       ' total parameter sets...\n')
            file.close()

        elif self.moi == 2:
            file = open('../../out/contourParams.dat', 'w')
            print('Find 2-axis quantization')
            for i1 in self.mois:
                for i2 in self.mois:
                    for i3 in self.mois:
                        for theta in self.thetas:
                            A3(self.spin0, i1, i2, i3, self.j, theta, file)
            file.close()
        else:
            print('No quantization chosen...')


start = time.time()
x = FindContourParams(1)
x.FindParams()
stop = time.time()

print(f'The thread slept for {stop-start} s...')