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

# 获取股票盈利能力数据
stock_profit = ts.get_profit_data(2019, 2)
data3 = stock_profit.loc[stock_profit['code'].isin(hs300),
                         ['code', 'roe', 'gross_profit_rate', 'net_profit_ratio']]
data3.columns = ['代码', 'ROE', '毛利率', '净利率']
data3 = round(data3, 2)
# print(data3)

# 获取成长能力数据
# nprg:净利润增长率(%)  nav:净资产增长率(%)
stock_growth = ts.get_growth_data(2019, 2)
data2 = stock_growth.loc[stock_growth['code'].isin(hs300), ['code', 'nprg']]
data2.columns = ['代码', 'NI增长率']
data2 = round(data2, 2)  # 保留2位小数
# print(data3)
'''
# 数据合并
hs300 = pd.merge(data1, data3, how='left', on='代码')
hs300 = hs300.drop_duplicates(inplace=True)  # 去除重复数据
#print(hs300.head())
'''

# 增加估值系数列
data1['估值系数'] = data1['PE'] * data1['PB']
data1 = round(data1, 2)
# print(data1.head())

# 数据合并进阶方法
merge = lambda x, y: pd.merge(x, y, how='left', on='代码')
merge_data = reduce(merge, [data1, data2, data3])
merge_data.drop_duplicates(inplace=True)
# print(merge_data)


# 条件选股
data_filterde = merge_data.loc[(merge_data['估值系数'] < 60) & (merge_data['ROE'] > 5),
                               ['代码', '名称', 'PE', 'PB', '估值系数', 'ROE', '收入%']]
# print('筛选结果共{}只个股'.format(len(data_filterde)))
# data_filterde.to_excel('D:/Data_analysis/nice300.xlsx')

# 按照字段对数据进行排序
data_filterde.sort_values(['估值系数'], ascending=True, inplace=True)
print(data_filterde.head())


# 数据分类
def map_func(x):
    '''
    作为apply函数的参数传入
    :param x : df 中一行或者一列数据,取决于apply函数的参数axis
    :return:将每个计算结果组合,返回一个series
    '''
    if x['ROE'] > 5:
        return '高成长'
    elif x['ROE'] >= 0:
        return '低成长'
    elif x['ROE'] < 0:
        return '亏损'


# 根据ROE数据计算"成长性"
merge_data['成长性'] = merge_data.apply(map_func, axis=1)
merge_data

# 对高成长分类按照"烟蒂系数"做升序排列
data_growth = merge_data[merge_data['成长性'] == "高成长"].sort_values(['估值系数'], ascending=True)
data_growth.head()

data_profit = merge_data[merge_data['成长性'] == "高成长"].sort_values(['ROE'], ascending=False)
data_profit.head()


def group_func(df):
    '''
    作为groupby.apply函数的参数传入
    :param df:实际是经过聚合后的单一类的 dataframe
    :return:返回df按照"烟蒂系数"排序后的前三位
    '''
    return df.sort_values(['估值系数'], ascending=True)[:2]


data_grouped = merge_data.groupby('成长性').apply(group_func)
data_grouped.head()

# 按照行业分类挑选估值系数最低的2只个股
data_grouped2 = merge_data.groupby('行业').apply(group_func)
data_grouped2.head()

