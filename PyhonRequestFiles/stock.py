import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web


class Stocks:
    def getdata():
        style.use('ggplot')

        start = dt.datetime(2009, 1, 1)
        end = dt.datetime.now()
        df = web.DataReader("AAPL", 'yahoo', start, end)
        return df

    def getdata(symbol):
        style.use('ggplot')

        start = dt.datetime(2009, 1, 1)
        end = dt.datetime.now()
        try:
            df = web.DataReader(symbol, 'yahoo', start, end)
            return df
        except:
            return pd.read_csv('CSVFiles/aapl.csv')

    def printdata(symbol):
        style.use('ggplot')

        start = dt.datetime(2009, 1, 1)
        end = dt.datetime.now()
        df = web.DataReader("DOX", 'yahoo', start, end)
        print(df)
        return df
