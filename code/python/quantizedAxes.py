import numpy as np
from timeit import default_timer as timer


def Axis(I1, I2, I3):
    if(I1 > I2 and I1 > I3 and I2 != I3):
        return 1
    elif(I2 > I1 and I2 > I3 and I1 != I3):
        return 2
    elif(I3 > I2 and I3 > I1 and I1 != I2):
        return 3
    return 0


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
    k = np.sqrt(uFunction(I, I1, I2, I3, j, theta))
    return k


def ValidParameters(I, I1, I2, I3, j, theta):
    u = uFunction(I, I1, I2, I3, j, theta)
    uChiral = uFunction(I, I1, I2, I3, j, theta+180)
    k = np.nan
    if(not u < 0):
        k = np.sqrt(u)
    A = AFunction(I, I1, I2, j, theta)
    AChiral = AFunction(I, I1, I2, j, theta+180)
    cond1 = 0
    cond2 = 0
    if(A > 0.0 and A < 1.0 and not np.isnan(AChiral)):
        cond1 = 1
    if(abs(u) < 1.0 and not np.isnan(uChiral) and not np.isnan(k)):
        cond2 = 1
    if(cond1 and cond2):
        return 1
    return 0


def ValidParameters3(I, I1, I2, I3, j, theta):
    u = uFunction(I, I1, I2, I3, j, theta)
    uChiral = uFunction(I, I1, I2, I3, j, theta+180)
    k = np.sqrt(abs(u))
    A = AFunction(I, I1, I2, j, theta)
    AChiral = AFunction(I, I1, I2, j, theta+180)
    cond1 = 0
    cond2 = 0
    if(A > 0.0 and A < 1.0 and not np.isnan(AChiral)):
        cond1 = 1
    if(abs(u) < 1.0 and not np.isnan(uChiral) and not np.isnan(k)):
        cond2 = 1
    if(cond1 and cond2):
        return 1
    return 0


steps = [10.0, 10.0]
mois = np.arange(1.0, 120.1, steps[0])
thetas = np.arange(-180.0, 180.1, steps[1])


def AxisQ(I, k):
    count = 0
    j = 5.5
    # store the valid parameters for later use
    paramset = []
    for I1 in mois:
        for I2 in mois:
            for I3 in mois:
                for th in thetas:
                    if(Axis(I1, I2, I3) == k):
                        if(k == 3):
                            vp = ValidParameters3(I, I1, I2, I3, j, th)
                        else:
                            vp = ValidParameters(I, I1, I2, I3, j, th)
                        if(vp):
                            count += 1
                            param_tuple = [I1, I2, I3, th]
                            paramset.append(param_tuple)
    return [paramset, count]


def ShowParams(I, k):
    filepath = '../../out/'
    name = f'paramSet-{k}axis'
    ext = '.dat'
    filename = filepath+name+ext

    j = 5.5
    start = timer()
    paramSet = AxisQ(I, k)[0]
    stop = timer()
    print(f'Computing the valid parameters for {k}-axis quantization:')
    print(f'The number of valid params is:   {AxisQ(I,k)[1]}')
    print(f'And the validity checker process took  {stop-start} s')
    file = open(filename, 'w')
    file.write('Fixed parameters: '+'I='+str(I)+' | j='+str(j)+'\n')
    file.write('The set of valid parameters for  ' +
               str(k)+'-axis quantization are:'+'\n')
    for p in paramSet:
        file.write('I1='+str(p[0])+'  I2='+str(p[1]) +
                   '  I3='+str(p[2])+' θ='+str(p[3])+'\n')

    file.close()


# paramSet=AxisQ(9.5,1)


ShowParams(9.5, 1)
ShowParams(9.5, 2)
ShowParams(9.5, 3)
