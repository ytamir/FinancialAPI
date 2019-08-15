import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style
from mpl_finance import candlestick_ohlc

style.use('ggplot')

# write the history of a stock to a file
# start = dt.datetime(2009, 1, 1)
# end = dt.datetime.now()
# df = web.DataReader("AAPL", 'yahoo', start, end)
# df.to_csv('AAPL.csv')


# df = pd.read_csv('DOX.csv')
df = pd.read_csv('AAPL.csv', parse_dates=True, index_col=0)
# print(df.head())
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

print(df_ohlc.head())
#print(df_volume)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()


candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup ='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)


plt.show()
##df['Adj CLose'].plot()
#plt.show()
# df['100ma'] = df['Adj Close'].rolling(window =100, min_periods=0).mean()
# df.dropna(inplace=True)
# print(df.head())