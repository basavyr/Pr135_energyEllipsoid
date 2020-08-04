import numpy as np


def Axis(I1, I2, I3):
    if(I1 > I2 and I1 > I3):
        return 1
    elif(I2 > I1 and I2 > I3):
        return 2
    elif(I3 > I2 and I3 > I1):
        return 3
    return 0

def AxisQ(k):
    I1 = 1
    I2 = 5
    I3 = 9
    print(Axis(I1,I2,I3))

AxisQ(1)