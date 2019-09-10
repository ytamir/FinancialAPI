import pandas as pd
import plotly.graph_objs as go
from PyhonRequestFiles.stock import Stocks
from dash.dependencies import Input, Output, State


def register_callbacks(app):

    @app.callback([Output('homepage-table', 'figure'),
                   Output('symbol', 'children')],
                  [Input('drop_down_symbols', 'value'),
                   Input('radio-items', 'value')])
    def plot_daily_high(input_symbols, candle_val):
        my_string = ''
        trace = []
        if input_symbols is not None:
            for symbol in input_symbols:
                stock_data = Stocks.getdata(symbol)
                stock_data.to_csv('CSVFiles/test.csv')
                stock_data_out = pd.read_csv("CSVFiles/test.csv")
                my_string = ', '.join(map(str, input_symbols))
                if candle_val == 'C':
                    trace.append(
                        go.Candlestick(x=stock_data_out['Date'], open=stock_data_out['Open'],
                                       high=stock_data_out['High'],
                                       low=stock_data_out['Low'], close=stock_data_out['Close'], name=symbol,
                                       increasing={'line': {'color': '#00CC94'}},
                                       decreasing={'line': {'color': '#F50030'}}))
                else:
                    trace.append(
                        go.Scatter(x=stock_data_out['Date'], y=stock_data_out['High'], name=symbol, mode='lines'))
            if candle_val == 'C':
                return {"data": trace, 'layout': go.Layout(title=f"Stock Values",
                                                           xaxis={'rangeslider': {'visible': False},
                                                                  'autorange': True, },
                                                           # if rangeslider is True then cannot change y axis range
                                                           yaxis={"title": f'Stock Price (USD)'})}, my_string
            else:
                return {"data": trace, 'layout': go.Layout(title=f"Stock Values",
                                                           xaxis={'rangeslider': {'visible': False},
                                                                  'autorange': True, },
                                                           yaxis={"title": f'Stock Price (USD)'})}, my_string
        else:
            return {'data': trace}, ""
