# -*- coding:utf-8 -*- 
'''
Created on 2019年1月24日

@author: Jimmy
'''
import time
import datetime
import tushare as ts
import numpy as np
from sqlalchemy import create_engine 


symbols = ['128036']
#mysql_engine = create_engine('mysql://root:abc123@localhost:3306/demos?charset=utf8&use_unicode=1')

"""
获取实时行情
"""
def get_realtime_price():
    for _ in range(3):
        try:
            df = ts.get_realtime_quotes(symbols)
            df = df[['code', 'price', 'volume', 'amount']]
            df = df.set_index('code')
            for col in df.columns:
                df[col] = df[col].astype(float)
        except:
            time.sleep(2)
        else:
            return df

    
def run():
    today  = datetime.datetime.today().date()
    today = str(today).replace('-', '')
    last = None
    while True:
        hour = datetime.datetime.today().hour
        minute = datetime.datetime.today().minute
        second = datetime.datetime.today().second
        if (hour > 15) or (hour == 9 and minute < 30) or (hour < 9) or (hour > 11 and hour < 13) or (hour == 11 and minute > 30):
            print('未开盘或已收市...')
            break
        else:
            this = get_realtime_price()
            if last is None:
                last = this
            else:
                df = this - last
                last = this
                df = df[(df.volume > 0) & (df.amount > 0) ]
                df.columns = ['change', 'volume', 'amount']
                this = this[['price']]
                df = df.merge(this, left_index=True, right_index=True, how='left')
                df['volume'] = df['volume'] / 100
                df['volume'] = df['volume'].astype(int)
                if df.shape[0] > 0:
                    df['date'] = today
                    df['time'] = '%s:%s:%s'%(str(hour).zfill(2), str(minute).zfill(2), str(second).zfill(2))
                    df = df.reset_index()
                    df['type'] = df['change'].map(lambda x: np.where(x>=0, '买入', '卖出'))
#                     df.to_sql('STOCK_TICK', mysql_engine, index=False, if_exists='append')
                    print(df)
        time.sleep(3)
        

def tick_test():
    df = ts.get_tick_data('300199', date='2019-01-22', src='tt')
    df['code'] = '300199'
    df['date'] = '20190122'
    df.to_sql('STOCK_TICK', mysql_engine, index=False, if_exists='append')
    print(df)

if __name__ == '__main__':
    run()
#     tick_test()    
    
    
    
    
    