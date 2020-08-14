import numpy as np
from timeit import default_timer as timer
import time
from numpy import random as rd
import matplotlib.pyplot as plt
params = [5.2, 1.9, 2.0, -0.1]
data_exp = [[1, 9.], [2, 8.9], [3, 8.8], [
    4, 8.7], [5, 8.6], [6, 8.5], [7, 8.4]]

xvalues = [1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5.,
           5.5, 6., 6.5, 7., 7.5, 8., 8.5, 9., 9.5, 10.]


def Fct(i1, i2, i3, th, x):
    return i1*np.sin(x)-i2*x+i3+th*x


def ExperimentalData(xvalues, params):
    expdata = []
    for x in xvalues:
        fx = Fct(params[0], params[1], params[2], params[3], x)
        if(fx == np.nan):
            return -1
        expdata.append(fx)
    if(len(expdata) == len(xvalues)):
        return expdata
    return -1


def CreatePlot(xdata, ydata):
    plt.plot(xdata, ydata[0], 'ok', label='Exp.')
    plt.plot(xdata, ydata[1], '-r', label='Th.')
    plt.legend(loc='best')
    plt.savefig('../../../out/rmsPLOT.pdf', bbox_inches='tight')
    plt.close()

mois = np.arange(1.5, 5.8, 0.2)
thetas = np.arange(-1.0, 1.0, 0.1)


def CreateParams():
    params_array = []
    for i1 in mois:
        for i2 in mois:
            for i3 in mois:
                for th in thetas:
                    tuplei = [i1, i2, i3, th]
                    params_array.append(tuplei)
    return params_array


params_array = CreateParams()


def GenerateTheoreticalData(exp_data, i1, i2, i3, th):
    th_data = []
    for id in exp_data:
        fx = Fct(i1, i2, i3, th, id[0])
        data_pair = [id[0], fx]
        th_data.append(data_pair)
    return th_data


test_th_data = GenerateTheoreticalData(
    data_exp, params[0], params[1], params[2], params[3])


def Compute_RMS(exp_data, th_data):
    if(len(exp_data) != len(th_data)):
        return np.nan
    sum_t = 0.0
    count = 0
    for id in range(len(exp_data)):
        if(th_data[id][1] == np.nan):
            return np.nan
        diff = (exp_data[id][1]-th_data[id][1])
        term = np.power(diff, 2)
        if(term != np.nan):
            count = count+1
            sum_t = sum_t+term
    if(count == len(exp_data)):
        return round(np.sqrt(sum_t/len(exp_data)), 5)
    else:
        return np.nan


def GetMinRMS(data_exp,params_array):
    start = timer()
    rms_array = []
    for p_set in params_array:
        data_th = GenerateTheoreticalData(
            data_exp, p_set[0], p_set[1], p_set[2], p_set[3])
        rms_array.append(Compute_RMS(data_exp, data_th))
    end = timer()
    min_params = params_array[rms_array.index(min(rms_array))]
    rms_array_sorted = np.sort(rms_array)
    min_rms = rms_array_sorted[0]
    print(f'The best parameters are: P={min_params}')
    print(f'The RMS of the data set is: {min_rms}')
    # print(rms_array)
    # print(rms_array_sorted)
    print(f'Process Duration: {(end-start)} seconds')
    thdata = ExperimentalData(xvalues, min_params)
    expdata = [ExperimentalData(xvalues, params), thdata]
    CreatePlot(xvalues, expdata)
    # print(params_array[rms_array.index(min(rms_array))])

# print(Compute_RMS(data_exp,test_th_data))

# GetMinRMS(params_array)


def PrintRMSResults(exp_data, params_array):
    print('Opening file...')
    file = open('../../../out/rms_test.dat', 'w')
    ok = 1
    for pars in params_array:
        th_data = GenerateTheoreticalData(
            exp_data, pars[0], pars[1], pars[2], pars[3])
        retval = Compute_RMS(exp_data, th_data)
        file.write(str(pars[0])+' '+str(pars[1]) +
                   ' ' + str(pars[2])+' '+str(pars[3]))
        file.write('  |  ')
        file.write(str(retval))
        file.write('\n')
        if(ok == 1):
            print('Writing data...')
            ok = 0
        # print(pars,retval)
    file.close()
    print('Closing file...')


new_expData = [[1., 4.37565], [1.5, 4.18697], [2., 2.72835], [2.5, 0.112055], [3., -3.26618], [3.5, -6.82407], [4., -9.93537], [4.5, -12.0832], [5., -12.9864], [5.5, -12.6688], [6., -11.453], [6.5,-9.88138], [7., -8.58367], [7.5, -8.1224], [8., -8.85534], [8.5, -10.8479], [9., -13.857], [9.5, -17.3908], [10., -20.8289]]

PrintRMSResults(new_expData, params_array)
GetMinRMS(new_expData,params_array)
