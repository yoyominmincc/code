import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ts.set_token("951c80115a1c647c011fc1b5115def083a1dfb55f989e6a9de0f6054")
pro = ts.pro_api()
'''
df = ts.get_hist_data('002548','2019-07-25')
df2 = ts.get_hist_data('300498','2019-07-25')

df.to_excel('D:/数据分析/0025482.xlsx')
df2.to_excel('D:/数据分析/3004982.xlsx')
'''
df = pro.cb_daily(ts_code='127010.SZ')
#df.to_excel('D:/Data_analysis/127010SZ.xlsx')

'''
df['group1']= np.random.choice(['a'])
grouped = df.groupby('group1')
#df2 = grouped.describe()
df2 = np.transpose(grouped.describe())
df2.to_excel('D:/Data_analysis/ddd127010SZ.xlsx')
'''

print("done!")