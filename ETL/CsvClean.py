import os
import pandas as pd
import numpy as np

basic_path='./csv'
csvs=os.listdir(basic_path)
print(csvs)

def splitHelps(column):
    return column.str.split(',')
for csv in csvs:
    df=pd.read_csv(basic_path+'/'+csv)
    cols=df.columns.tolist()
    print(cols)
    inplace=cols.index('Helpfulness')
    print(inplace)
    cols.insert(inplace+1,'AllHelps')
    print('cols',cols)
    df=df.reindex(columns=cols,fill_value=0)
    print(df.columns)
    ars=np.array(list(map(lambda x: np.array(x),df['Helpfulness'].str.split(','))))
    df['AllHelps'],df['Helpfulness']=ars[:,1],ars[:,0]
    df.to_csv(basic_path+'/'+csv,index=False)