import numpy as np
import pandas as pd
import tushare as ts
import seaborn
from matplotlib import pyplot as plt

stocks_pair = ['600199', '600702']

# 数据准备&回测准备
data1 = ts.get_k_data('600199', start='2019-01-01', end='2019-06-30')[['date', 'close']]
data2 = ts.get_k_data('600702', start='2019-01-01', end='2019-06-30')['close']
data = pd.concat([data1, data2], axis=1)
data.set_index('date', inplace=True)
data.columns = stocks_pair
data.plot(figsize=(8, 6))

# 策略开发思路
data['PriceDelta'] = data['600702'] - data['600199']
data['PriceDelta'].plot(figsize=(8, 6))
plt.ylabel('Spread')
plt.axhline(data['PriceDelta'].mean())
data['zscore'] = (data['PriceDelta'] - np.mean(data['PriceDelta'])) / np.std(data['PriceDelta'])  # 价差的标准化
data[data['zscore'] < -1.5]
len(data[data['zscore'] < -1.5])

data['position_1'] = np.where(data['zscore'] > 1.5, -1, np.nan)
data['position_1'] = np.where(data['zscore'] < -1.5, 1, data['position_1'])
data['position_1'] = np.where(abs(data['zscore']) < 0.5, 0, data['position_1'])
data.head()

# 产生交易信号
data['position_1'] = data['position_1'].fillna(method='ffill')
data['position_1'].plot(ylim=[-1.1, 1.1], figsize=(10, 6))  # 开仓头寸可视化
data['position_2'] = -np.sign(data['position_1'])
data.head()
data['position_2'].plot(ylim=[-1.1, 1.1], figsize=(10, 6))  # 开仓头寸可视化

# 计算策略年化收益并可视化
data['return_1'] = np.log(data['600199'] / data['600199'].shift(1))
data['return_2'] = np.log(data['600702'] / data['600702'].shift(1))
data.head()

data['strategy'] = 0.5 * (data['position_1'].shift(1) * data['return_1']) + 0.5 * (
        data['position_2'].shift(1) * data['return_2'])
data[['return_1', 'return_2', 'strategy']].dropna().cumsum().apply(np.exp).plot(figsize=(10, 6))

data.iloc[:, 1]  # index location,通过索引来获得数据,loc,ix
# 考虑时间序列平稳性
data1 = ts.get_k_data('600199', '2019-01-01', '2019-06-30')[['date', 'close']]
data2 = ts.get_k_data('600702', '2019-01-01', '2019-06-30')['close']
data = pd.concat([data1, data2], axis=1)

data.set_index('date', inplace=True)
data.columns = stocks_pair
data.head()
data.plot(figsize=(8, 6))

# 策略开发思路
data.corr()  # 方差和协方差矩阵

plt.figure(figsize=(10, 8))
plt.title('Stock Correlation')
plt.plot(data['600199'], data['600702'], '.')  # 画出散点图 ,看是否存在线性关系
plt.xlabel('600199')
plt.ylabel('600702')
data.dropna(inplace=True)

[slope, intercept] = np.polyfit(data.iloc[:, 0], data.iloc[:, 1], 1).round(2)
data['spread'] = data.iloc[:, 1] - (
        data.iloc[:, 0] * slope + intercept)  # ε = Y(702) - X(199)*斜率(slope) + 截距(intercept)
data.head()  # ε是stationary(υ=0,σ²)用来套利
data['spread'].plot(figsize=(10, 8), title='Price Spread')
data['zscore'] = (data['spread'] - data['spread'].mean()) / data['spread'].std()  # 标准化
data.head()

data['zscore'].plot(figsize=(10, 8), title='Z-score')
plt.axhline(1.5)
plt.axhline(0)
plt.axhline(-1.5)

# 产生交易信号
data['position_1'] = np.where(data['zscore'] > 1.5, 1, np.nan)  # 做多702
data['position_1'] = np.where(data['zscore'] < 1.5, -1, data['position_1'])  # 做空199
data['position_1'] = np.where(abs(data['zscore']) < 0.5, 0, data['position_1'])  # 不开仓
data['position_1'] = data['position_1'].fillna(method='ffill')
data['position_1'].plot(ylim=[-1.1, 1.1], figsize=(10, 6), title='Trading Signal_Uptrade')
data['position_2'] = -np.sign(data['position_1'])
data['position_2'].plot(ylim=[-1.1, 1.1], figsize=(10, 6), title='Trading Signal_Downtrade')

# 计算策略年化收益并可视化