# Testing the triaxial potential V(q) for different values of the parameter set
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
from datetime import datetime


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
    if(uFunction(I, I1, I2, I3, j, theta) >= 0.0):
        return np.sqrt(uFunction(I, I1, I2, I3, j, theta))
    return -1


def JacobiAmplitude(q, k):
    k2 = np.power(k, 2)
    JA = sp.ellipj(q, k2)
    return JA


def sn(q, k):
    return JacobiAmplitude(q, k)[0]


def cn(q, k):
    return JacobiAmplitude(q, k)[1]


def dn(q, k):
    return JacobiAmplitude(q, k)[2]


def JA(q, k):
    return JacobiAmplitude(q, k)[3]


def GenerateJAs(k):
    qValues = np.arange(-8, 8.1, 0.5)
    potential = []
    for q in qValues:
        V = JacobiAmplitude(q, k)[3]
        if(np.isnan(V) == False):
            potential.append(V)
    if(len(potential) == len(qValues)):
        return 'OK'
    return '!OK'


def Potential(q, I, I1, I2, I3, j, theta):
    k = kFunction(I, I1, I2, I3, j, theta)
    v0 = v0Function(I, I1, I2, j, theta)
    t1 = (I*(I+1)*np.power(k, 2)+np.power(v0, 2))
    s = sn(q, k)
    c = cn(q, k)
    d = dn(q, k)
    t2 = (2.0*I+1)*v0*c*d
    V = t1*np.power(s, 2)+t2
    return V


def WriteData(X, Y, file, dataname):
    if(len(X) != len(Y)):
        return
    file.write("(*Data batch generated at: "+str(datetime.utcnow())+"*)"+"\n")
    file.write(str(dataname)+"={ ")
    count = 0
    for id in range(len(X)):
        count = count+1
        s = "{"+str(round(float(X[id]), 3))+" , " + \
            str(Y[id])+"},"
        if(count == len(X)):
            s = "{"+str(round(float(X[id]), 3)) + \
                " , "+str(Y[id])+"}"
        file.write(s)
    file.write(" };\n")
    # file.write("ListLinePlot["+str(dataname)+"]")
    # file.write('\n')


qValues = np.arange(-8.0, 8.1, 0.25)


def CreatePotentialData(I, qValues):
    params = [I, 90, 100, 80, 5.5, -80]
    Vq = []
    for q in qValues:
        id_V = Potential(q, params[0], params[1],
                         params[2], params[3], params[4], params[5])
        Vq.append(id_V)
    return Vq


def CreatePotential(qValues, params):
    Vq = []
    for q in qValues:
        id_V = Potential(q, params[0], params[1],
                         params[2], params[3], params[4], params[5])
        Vq.append(id_V)
    return Vq


def PlotPotential(qData, IData):
    styles = ['-r', '--r', '-b', '--b', '-k', '--k']
    for I in IData:
        Vq = CreatePotentialData(I, qData)
        style = np.random.choice(styles)
        plt.plot(qData, Vq, style, label="I="+str(I))
    plt.legend(loc='best')
    plt.savefig('../../out/potential.pdf', bbox_inches='tight')
    plt.close()


spins = [7.5, 9.5, 11.5, 13.5]
params = [spins[1], 90.0, 100.0, 80.0, 5.5, -80]

AValues = []
kValues = []
uValues = []
v0Values = []

thetas = np.arange(-180.0, 180.5, 10.0)

for q in thetas:
    AValues.append(
        AFunction(params[0], params[1], params[2], params[4], q))
    kValues.append(
        kFunction(params[0], params[1], params[2], params[3], params[4], q))
    uValues.append(
        uFunction(params[0], params[1], params[2], params[3], params[4], q))
    v0Values.append(
        v0Function(params[0], params[1], params[2], params[4], q))

inertialData = [AValues, kValues, uValues, v0Values]
potentials = []

inertial_names = ['adata', 'kdata', 'udata', 'v0data']
potential_names = ['potential1', 'potential2', 'potential3', 'potential4']

for I in spins:
    potentials.append(CreatePotentialData(I, qValues))


def ShowDataToMathematica(xdata, YDATA, filename, names):
    count = 0
    f = open(filename, 'w')
    for y_data in YDATA:
        WriteData(xdata, y_data, f, names[count])
        count = count+1
    f.close()


# PlotPotential(qValues, spins)

# ShowDataToMathematica(thetas, inertialData,
#                       '../../out/inertialParams.dat', inertial_names)
# ShowDataToMathematica(qValues, potentials,
#                       '../../out/potentials.dat', potential_names)


# Vq = CreatePotentialData(spins[1], qValues)

# f = open('test.dat', 'w')
# WriteData(qValues, Vq, f)
# f.close()

def Pset(theta):
    params = [9.5, 80, 100, 90, 5.5, theta]
    return params


V1 = CreatePotential(qValues, Pset(-80))
V2 = CreatePotential(qValues, Pset(100))
print(V1)
print(V2)
