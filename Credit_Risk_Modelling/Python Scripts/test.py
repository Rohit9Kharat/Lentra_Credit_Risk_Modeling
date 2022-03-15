
import pandas as pd
import numpy as np

df = pd.read_csv("a.csv")

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def CheckForInBetween(list1, val1, val2):
    #return(any(x >= val1 for x in list1) and any(x <= val2 for x in list1))
    return any(list(x for x in list1 if val1 <= x <= val2))

dpd30_3m = list()
dpd60_3m = list()
dpd90_3m = list()
matching = list()

for x in range(0, df.shape[0]):
    if (df['mo_diff_ld_drc'][x] == -1):
        dpd30_3m.append('unknown')
        dpd60_3m.append('unknown')
        dpd90_3m.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 4):
        for i in range(0, 3):
            if hasNumbers(df['payHistComp'][x][i]):
                a = int(df['payHistComp'][x][i])
                matching.append(a)
            else:
                continue
        #print(matching)
        if CheckForInBetween(matching, 1, 30):
            dpd30_3m.append(1)
            #print('1',matching)
        if CheckForInBetween(matching, 31, 60):
            dpd60_3m.append(1)
            #print('2',matching)
        if CheckForInBetween(matching, 61, 90):
            dpd90_3m.append(1)
            #print('3',matching)
        elif (not CheckForInBetween(matching, 1, 90)):
            #print(matching)
            dpd30_3m.append(0)
            dpd60_3m.append(0)
            dpd90_3m.append(0)
        #print(matching)
        matching = list()
    else:
        #print(matching)
        dpd30_3m.append(0)
        dpd60_3m.append(0)
        dpd90_3m.append(0)

df['DPD30P3M_flag'] = pd.Series(dpd30_3m).values
#df['DPD60P3M_flag'] = pd.Series(dpd60_3m).values
#df['DPD90P3M_flag'] = pd.Series(dpd90_3m).values

#df['DPD30P3M_flag'].value_counts()
