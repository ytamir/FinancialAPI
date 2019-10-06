import pandas as pd
import plotly.graph_objs as go
from PyhonRequestFiles.MachineLearning import ML
from PyhonRequestFiles.stock import Stocks

from dash.dependencies import Input, Output


def register_callbacks(app):
    @app.callback(Output('ml-table', 'figure'),
                  [Input('ml_dropdown', 'value')])
    def plot_daily_high(input_symbols):
        print('hello')
        x_axis_seq, data, mid_data = ML.getdata(input_symbols)
        best_prediction_epoch = 13
        trace = []
        xvals = []
        yvals = []
        count = int(mid_data.size*.7)
        for val in mid_data[int(mid_data.size*.7):]:
            xvals.append(count)
            yvals.append(val)
            count = count + 1
        print(xvals)
        print(yvals)
        trace.append(go.Scatter( x=xvals , y=yvals, mode='lines'))
        for xval, yval in zip(x_axis_seq, data[best_prediction_epoch]):
            trace.append(go.Scatter(x=xval, y=yval, mode='lines'))
        return {'data': trace}
