import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2009, 1, 1)
end = dt.datetime.now()

df = web.DataReader("AAPL", 'yahoo', start, end)
df.to_csv('AAPL.csv')
# df = pd.read_csv('DOX.csv')
#df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
print(df.head())
##df['Adj CLose'].plot()
plt.show()
# df['100ma'] = df['Adj Close'].rolling(window =100, min_periods=0).mean()
# df.dropna(inplace=True)
# print(df.head())