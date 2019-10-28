import plotly.graph_objs as go
from PyhonRequestFiles.StockPrice import Stocks
from dash.dependencies import Input, Output
import json

#def register_callbacks(app):

    # @app.callback(Output('homepage-table', 'figure'),
    #               [Input('drop_down_symbols', 'value'),
    #                Input('home_radio-items', 'value'),
    #                Input('time_radio-items', 'value')])
def register_callbacks(app):    
    @app.route('/get/daily_price/<tickers>/<candle_val>/<time_val>', methods=['GET'])
    def plot_daily_high(tickers, candle_val, time_val):
        trace = []
        print('tickers')
        print(tickers)
        ticekrsarr = tickers.split(',')
        if tickers is not None:
            for symbol in ticekrsarr:
                stock = {'name': symbol}                
                stock_data = Stocks.get_data_daily(symbol, time_val)
                stock['stock_data'] = stock_data.to_json()                
                trace.append(stock)
            return json.dumps(trace)
        else:
            return {}
