import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tushare as ts

#ds = ts.get_hist_data('300498')
#ds.to_excel('d:/数据分析/300498.xlsx')

xjn = pd.read_excel('d:/数据分析/002548.xlsx',index_col='date')
ws = pd.read_excel('d:/数据分析/300498.xlsx',index_col='date')




"""
df['close'].plot(label='002548',figsize=(8,3))
df2['close'].plot(label='300498')

spread = xjn['close']/ws['close']
spread_mean = spread.mean()
spread.plot(label='spread')

plt.axhline(y=spread_mean,color='red')
plt.tick_params(labelsize=8)
plt.xticks(rotation=60)
plt.xlabel('date')
plt.ylabel('Price')
plt.grid()
plt.show()
"""

#print(df.head())
#print(df2.head())
