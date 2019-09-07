import pandas as pd
import matplotlib.pyplot as plt


#cost = ts.get_hist_data('002548')
data = pd.read_excel('D:/数据分析/002548.xlsx',index_col='date')

data.plot(y=['close','open','high','low'])
plt.title("2016-2019price",fontsize=12,fontweight='bold')
plt.ylabel("price",fontsize=12,fontweight='bold')
plt.xlabel("date",fontsize=12,fontweight='bold')
plt.xticks(rotation=60)
#plt.savefig("filename.png",dpi=1200)
plt.show()

#data = pd.read_excel('D:/数据分析/000875.xlsx',index_col='date')
#data.sort_values(by='high',inplace=True,ascending=False)
#data.plot.bar(x='high')
#plt.show()