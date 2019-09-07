import tushare as ts
import pandas as pd

def Multiple_stocks(tickers):
    def data(ticker):
        stocks = ts.get_k_data(ticker,start='2019-07-01',end='2019-08-18')
        stocks.set_index('date', inplace=True)
        stocks.index = pd.to_datetime(stocks.index)
        return stocks


    datas = map(data, tickers)

    return pd.concat(datas, keys=tickers, names=['Ticker', 'trade_date'])


tickers = ['600030','000679']
all_stocks = Multiple_stocks(tickers)
print(all_stocks.head(50))