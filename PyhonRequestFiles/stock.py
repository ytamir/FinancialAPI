import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import csv


def getapikey():
    with open('CSVFiles/apikey.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            print('row')
            print(row)
            return row[0]


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
            print(df.head())
            stock_data = df
            stock_data.to_csv('test.csv')
            stock_data_out = pd.read_csv("test.csv")
            print(stock_data_out['Date'].head())
            # return df

        except:
            return pd.read_csv('CSVFiles/aapl.csv')

    def getdatadaily(symbol):
        key = getapikey()
        ts = TimeSeries(key, output_format='pandas', indexing_type='date')
        # data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        data.rename(columns={'date': 'Date',
                             '1. open': 'Open',
                             '2. high': 'High',
                             '3. low': 'Low',
                             '4. close': 'Close',
                             '5. volume': 'Volume'},
                    inplace=True)
        return data
        #  df = df.T.reset_index(drop=True).T

    def printdata(symbol):
        style.use('ggplot')

        start = dt.datetime(2009, 1, 1)
        end = dt.datetime.now()
        df = web.DataReader("DOX", 'yahoo', start, end)
        print(df)
        return df


