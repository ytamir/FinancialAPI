import pandas as pd
import plotly.graph_objs as go
from PyhonRequestFiles.stock import Stocks
from dash.dependencies import Input, Output


def register_callbacks(app):
    @app.callback(Output('homepage-table', 'figure'),
                  [Input('drop_down_symbols', 'value'),
                   Input('home_radio-items', 'value'),
                   Input('time_radio-items', 'value')])
    def plot_daily_high(input_symbols, candle_val, time_val):
        trace = []
        if input_symbols is not None:
            for symbol in input_symbols:
                stock_data = Stocks.getdatadaily(symbol, time_val)
                if candle_val == 'C':
                    trace.append(
                        go.Candlestick(x=stock_data['Date'], open=stock_data['Open'],
                                       high=stock_data['High'],
                                       low=stock_data['Low'], close=stock_data['Close'], name=symbol,
                                       increasing={'line': {'color': '#00CC94'}},
                                       decreasing={'line': {'color': '#F50030'}}))
                else:
                    trace.append(
                        go.Scatter(x=stock_data['Date'], y=stock_data['High'], name=symbol, mode='lines'))
            if candle_val == 'C':
                return {"data": trace, 'layout': go.Layout(title=f"Stock Values",
                                                           xaxis={'rangeslider': {'visible': False},
                                                                  'autorange': True, },
                                                           # if rangeslider is True then cannot change y axis range
                                                           yaxis={"title": f'Stock Price (USD)'})}
            else:
                return {"data": trace, 'layout': go.Layout(title=f"Stock Values",
                                                           xaxis={'rangeslider': {'visible': False},
                                                                  'autorange': True, },
                                                           yaxis={"title": f'Stock Price (USD)'})}
        else:
            return {'data': trace}
