import numpy as np
import pandas as pd
import tushare as ts

data = ts.get_k_data('hs300', start='2015-01-01', end='2019-09-12')
# data = pd.DataFrame(data)   把data转化成为DataFrame
data.rename(columns={'close': 'price'}, inplace=True)
# data.info()
data.set_index('date', inplace=True)
# data.head()

data['SMA_10'] = data['price'].rolling(10).mean()  # 必背
data['SMA_60'] = data['price'].rolling(60).mean()
# data.tail()

data[['price', 'SMA_10', 'SMA_60']].plot(title='HS300 stock price | 10 & 60 days SMAs',
                                         figsize=(10, 6))  # pandas里的多列选择要掌握

# 策略开发思路
data['position'] = np.where(data['SMA_10'] > data['SMA_60'], 1, -1)
data.dropna(inplace=True)  # 去掉空值,NaN
data['position'].plot(ylim=[-1.1, 1.1], title="Market Positioning")

# 计算策略年化收益并可视化
data['returns'] = np.log(data['price'] / data['price'].shift(1))  # Numpy向量化;循环做法(尽量避免),连续return
data['returns_dis'] = data['price'] / data['price'].shift(1) - 1  # 离散计算return方法1
data['returns_dis2'] = data['price'].pct_change()  # 离散计算return方法2
data['returns'].hist(bins=35)

data['strategy'] = data['position'].shift(1) * data['returns']  # shift避免了未来函数

# 策略风险评估
data[['returns', 'strategy']].mean() * 252  # 年化收益率
data[['returns', 'strategy']].std() * 252 ** 0.5  # 年化风险
data['cumret'] = data['strategy'].cumsum().apply(np.exp)  # 累计收益
data['cummax'] = data['cumret'].cummax()  # 累计收益某一时间段中的最大值
data[['cumret', 'cummax']].plot(figsize=(10, 6))
drawdown = (data['cummax'] - data['cumret'])
drawdown.max()  # 计算原理:最大回测;
temp = drawdown[drawdown == 0]
periods = (temp.index[1:].to_datetime() - temp.index[:-1].to_datetime())
periods.max()

# 策略优化的一种思路
hs300 = ts.get_k_data('hs300', start='2016-01-01', end='2019-9-14')[['date', 'close']]
hs300.rename(columns={'close': 'price'}, inplace=True)
hs300.set_index('date', inplace=True)
hs300.head()
hs300['SMA_10'] = hs300['price'].rolling(10).mean()  # 必背
hs300['SMA_60'] = hs300['price'].rolling(60).mean()  # 必背
hs300[['price', 'SMA_10', 'SMA_60']].plot(grid=True, figsize=(10, 8))
hs300['10-60'] = hs300['SMA_10'] - hs300['SMA_60']
hs300['10-60'].tail()

SD = 50  # 阈值
hs300['regime'] = np.where(hs300['10-60'] > SD, 1, 0)
hs300['regime'] = np.where(hs300['10-30'] < -SD, -1, hs300['regime'])
hs300['regime'].value_counts()  # 计数函数

hs300['Market'] = np.log(hs300['price'] / hs300['price'].shift(1))
hs300['Strategy'] = hs300['regime'].shift(1) * hs300['Market']  #1时获得收益 0时空仓 -1时做空
hs300[['Market', 'Strategy']].cumsum().apply(np.exp).plot(grid=True, figsize=(10, 6))

