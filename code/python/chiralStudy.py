import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp

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
    A1 = MOI(I1)
    A2 = MOI(I2)
    j2 = j_AM(j, theta)[1]
    return A2*(1.0-(j2/I))-A1


def v0(I, I1, I2, j, theta):
    A1 = MOI(I1)
    j1 = j_AM(j, theta)[0]
    return (-1.0)*(A1*j1)/A(I, I1, I2, j, theta)


def u(I, I1, I2, I3, j, theta):
    A1 = MOI(I1)
    A3 = MOI(I3)
    return (A3-A1)/A(I, I1, I2, j, theta)

# study the difference of the two inertia factors involved in this function


def U_DIFF(I, I1, I2, I3, j, theta):
    A1 = MOI(I1)
    A3 = MOI(I3)
    return [(A3-A1)/A(I, I1, I2, j, theta), A3-A1]


def k(I, I1, I2, I3, j, theta):
    uparam = u(I, I1, I2, I3, j, theta)
    if(uparam >= 0.0):
        return np.sqrt(uparam)
    return np.sqrt(abs(uparam))


# storing the value of the Jacobi Amplitude
def JA(q, m):
    m2 = np.power(m, 2)
    jacobi = sp.ellipj(q, m2)[3]
    return jacobi


def SN(q, m):
    return np.sin(JA(q, m))


def CN(q, m):
    return np.cos((JA(q, m)))


def DN(q, m):
    s = SN(q, m)
    return np.sqrt(1.0-m*m*s*s)


def Vq(q, I, I1, I2, I3, j, theta):
    k_p = k(I, I1, I2, I3, j, theta)
    v_p = v0(I, I1, I2, j, theta)
    s_p = SN(q, k_p)
    c_p = CN(q, k_p)
    d_p = DN(q, k_p)
    T1 = (I*(I+1.0)*k_p*k_p+v_p*v_p)*s_p*s_p
    T2 = (2.0*I+1.0)*v_p*c_p*d_p
    return T1+T2


qValues = np.arange(-8.0, 8.1, 0.25)
thetas = np.arange(-180.0, 180.1, 10.0)


def ParamSet(params, theta):
    P = [params[0], params[1], params[2], params[3], params[4], theta]
    P_chiral = [params[0], params[1], params[2],
                params[3], params[4], theta+180]
    param_set = [P, P_chiral]
    return param_set


def CreatePotential(params, theta):
    V = []
    VChiral = []
    params = ParamSet(params, theta)
    P = params[0]
    P_chiral = params[1]
    for q in qValues:
        current_V = Vq(q, P[0], P[1], P[2], P[3], P[4], P[5])
        current_VChiral = Vq(
            q, P_chiral[0], P_chiral[1], P_chiral[2], P_chiral[3], P_chiral[4], P_chiral[5])
        V.append(current_V)
        VChiral.append(current_VChiral)
    potentials = [V, VChiral]
    return potentials


def PlotPotential(params, theta):
    title = 'chiralPotential.pdf'
    filename = '../../out/'+title
    V = CreatePotential(params, theta)
    # V[0] is the normal triaxial potential, for a value of coupling angle theta
    # V[1] is the potential for the chiral transformation on the nucleus, with the angle theta=theta+pi
    plt.plot(qValues, V[0], '-b', label=f'$V$')
    plt.plot(qValues, V[1], '-r', label=f'$V_c$')
    plt.legend(loc='best')
    plt.savefig(filename, bbox_inches='tight')


params = [9.5, 85, 100,  65, 5.5]

thval = -80.0
thval_chiral = thval+180.0
PlotPotential(params, thval)
print(f'Params for th={thval}')
print(k(params[0], params[1], params[2], params[3], params[4], thval))
print(v0(params[0], params[1], params[2], params[4], thval))
print(Vq(0.0, params[0], params[1], params[2], params[3], params[4], thval))
print('########################')
print(f'Params for th={thval_chiral}')
print(k(params[0], params[1], params[2], params[3], params[4], thval_chiral))
print(v0(params[0], params[1], params[2], params[4], thval_chiral))
print(Vq(0.0, params[0], params[1], params[2],
         params[3], params[4], thval_chiral))


print('######### V(q) ##########')
print('#########################')
# output the potential values for testing purposes
for q in qValues:
    print("#",q, Vq(q, params[0], params[1],
                params[2], params[3], params[4], thval_chiral))
print('########################')
