import pandas as pd
import numpy as np
from datetime import datetime

import seaborn as sna

period = pd.date_range('2018-1-1', periods=10000, freq='D')
df = pd.DataFrame(np.random.randn(10000, 4), columns=['Date1', 'Date1', 'Date3', 'Date4'], index=period)

df.loc['data'] = pd.to_datetime(df.loc['data'])
print(df.head())
