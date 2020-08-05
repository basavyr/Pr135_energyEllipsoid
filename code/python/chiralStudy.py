import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

# Document used for plotting the values of the triaxial potential for a fixed coupling angle
# The implementation will plot V(q) and V_chiral(q), where the latter is computed by applying a chiral transformation on the first value of theta


def MOI(I):
    return 1.0/(2.0*I)


def j_AM(j, theta):
    theta_degrees = theta*np.pi/180.0
    j1 = j*np.cos(theta_degrees)
    j2 = j*np.sin(theta_degrees)
    single_particle_AM = [j1, j2]
    return single_particle_AM


def A(I, I1, I2, j, theta):
    return 'A'


def v0(I, I1, I2, j, theta):
    return 'v0'


def u(I, I1, I2, I3, j, theta):
    return 'u'


def k(I, I1, I2, I3, j, theta):
    return 'k'


def Vq(q, I, I1, I2, I3, j, theta):
    return 'V(q)'


qValues = np.arange(-8.0, 8.1, 0.5)
thetas = np.arange(-180.0, 180.1, 10.0)


def ParamSet(I, theta):
    P = [I, 80, 100, 90, 5.5, theta]
    P_chiral = [I, 80, 100, 90, 5.5, theta+180]
    param_set = [P, P_chiral]
    return param_set


def CreatePotential(I, theta):
    V = []
    VChiral = []
    P = ParamSet(I, theta)[0]
    P_chiral = ParamSet(I, theta)[1]
    for q in qValues:
        current_V = Vq(q, P[0], P[1], P[2], P[3], P[4], P[5])
        current_VChiral = Vq(
            q, P_chiral[0], P_chiral[1], P_chiral[2], P_chiral[3], P_chiral[4], P_chiral[5])
        V.append(current_V)
        VChiral.append(current_VChiral)
    potentials = [V, VChiral]
    return potentials

# def PlotPotential(spin, theta):
