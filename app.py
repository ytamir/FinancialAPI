import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
# from GetStockRowData import StockRowData
import plotly.graph_objs as go
from stock import Stocks


df = Stocks.getdata()
# df = StockRowData.get_file("GOOGL", SheetType.METRICS, Frequency.QUARTERLY)
# df['Short Date']= pd.to_datetime(df['DATE'])
# df['Short Date'] = df['Short Date'].apply(lambda x:x.date().strftime('%m%d%y'))
# df.to_csv("test.csv", index=False)

df.to_csv('test.csv')
fd = pd.read_csv("test.csv")
dff = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
print("df")
print (df)
print('dff')
print(dff)
print('fd')
print(fd)
#print('fd')
#print(fd)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='AAPL Stock'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

   dcc.Graph(
    id='table',
    figure = {
        'data': [
            go.Scatter(x=fd['Date'], y=fd['High'])
        ]
        }
)
])

if __name__ == '__main__':
    app.run_server(debug=True)