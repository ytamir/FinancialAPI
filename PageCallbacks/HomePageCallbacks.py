import pandas as pd
import plotly.graph_objs as go
from PyhonRequestFiles.stock import Stocks
from dash.dependencies import Input, Output, State


def register_homepage_callbacks(app, init_stock):

    @app.callback([Output('table', 'figure'),
                   Output('symbol', 'children')],
                  [Input('submit-button', 'n_clicks')],
                  [State('drop_down_symbols', 'value')])
    def plot_daily_high(n_clicks, input_symbols):

        if input_symbols is not None:
            trace = []
            for symbol in input_symbols:
                stock_data = Stocks.getdata(symbol)
                stock_data.to_csv('CSVFiles/test.csv')
                stock_data_out = pd.read_csv("CSVFiles/test.csv")
                trace.append(go.Scatter(x=stock_data_out['Date'], y=stock_data_out['High'], name=symbol, mode='lines'))
            my_string = ', '.join(map(str, input_symbols))
            return {"data": trace}, my_string
        else:
            return {
                       'data': [
                           go.Scatter(x=init_stock['Date'], y=init_stock['High'])
                       ]
                   }, "AAPL"
