import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tushare as ts
from functools import reduce

'''
hs300 = ts.get_hist_data('hs300',start='2019-01-01',end='2019-08-31')
#hs300['close'].plot(figsize=(8,5),grid=True,title='hs300close')
hs300['return'] = np.log(hs300['close']/hs300['close'].shift(1))#计算连续收益
lk = hs300[['close','return']].tail()
print(lk)
'''

# 获取hs300股票信息
hs300 = ts.get_hs300s()['code'].tolist()  # 转化成list

# 获取基本面数据
# rev:收入同比(%)  profit:利润同比(%) npr:净利润率(%)
stock_basics = ts.get_stock_basics()
stock_basics.reset_index(inplace=True)
data1 = stock_basics.loc[stock_basics['code'].isin(hs300),  # 从大表中把hs300的代码挑选出来
                         ['code', 'name', 'industry', 'pe', 'pb', 'esp', 'rev', 'profit', ]]
data1.columns = ['代码', '名称', '行业', "PE", 'PB', 'EPS', '收入%', '利润%']

# 获取成长能力数据
# nprg:净利润增长率(%)  nav:净资产增长率(%)
stock_growth = ts.get_growth_data(2019, 2)
data2 = stock_growth.loc[stock_growth['code'].isin(hs300), ['code', 'nprg']]
data2.columns = ['代码', 'NI增长率']
data2 = round(data2, 2)  # 保留2位小数

# 数据合并
hs300 = pd.merge(data1, data2, how='left', on='代码')
hs300.drop_duplicates(inplace=True)  # 去除重复数据
print(hs300.head())
# 进阶方法
merge = lambda x, y: pd.merge(x, y, how='left', on='代码')
merge_data = reduce(merge, [data1, data2])
merge_data.drop_duplicates(inplace=True)
