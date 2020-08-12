import numpy as np

params=[5.2,1.9,2.0,-0.1]
data_exp=[[1,9.],[2,8.9],[3,8.8],[4,8.7],[5,8.6],[6,8.5],[7,8.4]]

def Fct(i1,i2,i3,th,x):
    return i1+i2+i3+th*x

mois=np.arange(1.0,6.1,0.5)
thetas=[-10.0,10.1,0.1]

params_array=[]

def CreateParams(params_array):
    for i1 in mois:
        for i2 in mois:
            for i3 in mois:
                for th in thetas:
                    tuple=[i1,i2,i3,th]
                    params_array.append(tuple)
    return params_array

CreateParams(params_array)

def GenerateTheoreticalData(exp_data,i1,i2,i3,th):
    th_data=[]
    for id in range(len(exp_data)):
        fx=Fct(i1,i2,i3,th,exp_data[id][0])
        data_pair=[exp_data[id][0],fx]
        th_data.append(data_pair)
    return th_data


def Compute_RMS(exp_data,th_data):
    if(len(exp_data)!=len(th_data)):
        return np.nan
    sum=0.0
    count=0
    for id in range(len(exp_data)):
        if(th_data[id][1]==np.nan):
            return np.nan
        diff=(exp_data[id][1]-th_data[id][1])
        term=np.power(diff,2)
        if(term!=np.nan):
            count= count+1
        sum=sum+term
    if(count==len(exp_data)):
        return round(np.sqrt(sum/len(exp_data)),3)
    else:
        return np.nan

rms_array=[]


for set in params_array:
    data_th=GenerateTheoreticalData(data_exp,set[0],set[1],set[2],set[3])
    rms_array.append(Compute_RMS(data_exp,data_th))
    # print(Compute_RMS(data_exp,data_th))


print(params_array[rms_array.index(min(rms_array))])
rms_array=np.sort(rms_array)
print(rms_array[0])
# print(Compute_RMS(data_exp,data_th))