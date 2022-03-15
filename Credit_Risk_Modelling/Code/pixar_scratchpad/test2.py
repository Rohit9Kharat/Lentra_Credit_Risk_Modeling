import pandas as pd
import numpy as np
import datetime

list_of_dates = ['2019-11-20', '2020-01-02', '2020-02-05','2020-03-10','2020-04-16','2020-05-01']
employees=['Hisila', 'Shristi','Zeppy','Alina','Jerry','Kevin']
df = pd.DataFrame({'Joined date': pd.to_datetime(list_of_dates)},index=employees)

mask = (df['Joined date'] > '2019-06-1') & (df['Joined date'] <= '2020-02-05')
filtered_df=df.loc[mask]
print(filtered_df)

b = ['a', ' b', 'c ', ' d ']
d =['b','d']

for i, s in enumerate(b):
    if True:
        b = list(set(b)-set(d))


days = [-370, -321, -298, -90, -40, 26, 481]

d= filter(lambda x: x >= -90 & x<0, days)


from collections import Counter
myList = [1,4,6,7,8]

c = Counter(myList)

a =sum([k for k,v in c.items() if v == 2])
