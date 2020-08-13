import numpy as np
from timeit import default_timer as timer
import time
from numpy import random as rd

params = [5.2, 1.9, 2.0, -0.1]
data_exp = [[1, 9.], [2, 8.9], [3, 8.8], [
    4, 8.7], [5, 8.6], [6, 8.5], [7, 8.4]]


def Fct(i1, i2, i3, th, x):
    return i1+i2+i3+th*x


mois = np.arange(1.5, 6.0, 0.5)
thetas = np.arange(-1.0, 1.0, 0.1)


def CreateParams():
    params_array=[]
    for i1 in mois:
        for i2 in mois:
            for i3 in mois:
                for th in thetas:
                    tuplei = [i1, i2, i3, th]
                    params_array.append(tuplei)
    return params_array


params_array=CreateParams()


def GenerateTheoreticalData(exp_data, i1, i2, i3, th):
    th_data = []
    for id in exp_data:
        fx = Fct(i1, i2, i3, th, id[0])
        data_pair = [id[0], fx]
        th_data.append(data_pair)
    return th_data


test_th_data=GenerateTheoreticalData(data_exp,params[0],params[1],params[2],params[3])

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
        return round(np.sqrt(sum_t/len(exp_data)),5)
    else:
        return np.nan


def GetMinRMS(params_array):
    start = timer()
    rms_array = []
    for set in params_array:
        data_th = GenerateTheoreticalData(
            data_exp, set[0], set[1], set[2], set[3])
        rms_array.append(Compute_RMS(data_exp, data_th))
    end = timer()
    min_params = params_array[rms_array.index(min(rms_array))]
    rms_array_sorted = np.sort(rms_array)
    min_rms = rms_array[0]
    # print(f'The best parameters are: P={min_params}')
    # print(f'The RMS of the data set is: {min_rms}')
    print(rms_array)
    print(rms_array_sorted)
    print(f'Process Duration: {(end-start)} seconds')
    # print(params_array[rms_array.index(min(rms_array))])

# print(Compute_RMS(data_exp,test_th_data))

# GetMinRMS(params_array)

def PrintRMSResults(exp_data,params_array):
    print('Opening file...')
    file=open('../../../out/rms_test.dat','w')
    ok=1
    for pars in params_array:
        th_data=GenerateTheoreticalData(exp_data,pars[0],pars[1],pars[2],pars[3])
        retval=Compute_RMS(exp_data,th_data)
        file.write(str(pars[0])+' '+str(pars[1])+' ' +str(pars[2])+' '+str(pars[3]))
        file.write('  |  ')
        file.write(str(retval))
        file.write('\n')
        if(ok==1):
            print('Writing data...')
            ok=0
        # print(pars,retval)
    file.close()
    print('Closing file...')

PrintRMSResults(data_exp,params_array)