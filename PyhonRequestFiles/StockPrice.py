from matplotlib import style
from alpha_vantage.timeseries import TimeSeries

import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import csv


def getapikey():
    with open('CSVFiles/apikey.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            return row

class Stocks:
    def get_apple_data():
        style.use('ggplot')
        start = dt.datetime(1980, 1, 1)
        end = dt.datetime.now()
        df = web.DataReader("AAPL", 'yahoo', start, end)
        return df

    def get_yahoo_finance_data(symbol):
        print('Symbol')
        print(symbol)
        style.use('ggplot')
        start = dt.datetime(1980, 1, 1)
        end = dt.datetime.now()
        try:
            df = web.DataReader(symbol, 'yahoo', start, end)
            df.reset_index(inplace=True)
            return df
        except:
            return pd.read_csv('CSVFiles/aapl.csv').reset_index(inplace=True)

    def get_aa_timesereis(key, symbol, time_val):
        ts = TimeSeries(key, output_format='pandas', indexing_type='date')
        if time_val == 'd':
            data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        else:
            data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
        data.reset_index(inplace=True)
        data.rename(columns={'date': 'Date',
                             '1. open': 'Open',
                             '2. high': 'High',
                             '3. low': 'Low',
                             '4. close': 'Close',
                             '5. volume': 'Volume'},
                    inplace=True)
        return data

    def get_data_daily(symbol, time_val):
        keylist = getapikey()
        for key in keylist:
            try:
                return Stocks.get_aa_timesereis(key, symbol, time_val)
            except:
                # next key
                continue
        return Stocks.get_yahoo_finance_data(symbol)
