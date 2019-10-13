import pandas as pd
import plotly.graph_objs as go
from PyhonRequestFiles.MachineLearning import ML

from dash.dependencies import Input, Output


def register_callbacks(app):
    @app.callback(Output('ml-table', 'figure'),
                  [Input('ml_dropdown', 'value')])
    def plot_daily_high(input_symbol):
        print('hello')
        df, x_axis_seq, data, mid_data = ML.getdata(input_symbol)
        best_prediction_epoch = 13
        colorway = ['#00ffad', '#49edc6', '#4fdec8', '#51cfc9', '#51c1c7', '#4fb4c5', '#4ba6c2', '#4799be', '#438cba',
                    '#3d7fb6', '#3672b1', '#2e66ad', '#245aa8', '#174ea2', '#00429d']
        colorway2 = ['#00876c', '#3b976c', '#5fa66c', '#81b56c', '#a4c26d', '#c9cf71', '#eeda7a', '#efc265', '#efa956',
                     '#ec904e', '#e7754b', '#df5a4c', '#d43d51', '#49edc6', '#4fdec8', '#51cfc9', '#51c1c7']
        colorwaygreytored = ['#808080', '#8b7575', '#956b6b', '#a06060', '#aa5656', '#b54b4b', '#c04141', '#ca3636',
                             '#d52b2b', '#df2121', '#ea1616', '#f40c0c', '#ff0101', '#4fdec8', '#51cfc9', '#51c1c7']
        trace = []
        xvals = []
        yvals = []
        count = int(mid_data.size * .7)
        for val in mid_data[int(mid_data.size * .7):int(mid_data.size * .85)]:
            xvals.append(df.ix[count, "Date"])
            yvals.append(val)
            count = count + 1
        trace.append(go.Scatter(x=xvals, y=yvals, mode='lines', line={'color': '#808080'}))

        colorcount = 0
        for preds in data:
            for xval, yval, color in zip(x_axis_seq, preds, colorway):
                trace.append(go.Scatter(x=xval['Date'], y=yval, mode='lines',
                                        name="Attempt " + str(colorcount),
                                        line={'color': colorway[colorcount]}))
            colorcount = colorcount + 1
        layout = go.Layout(colorway=colorway)

        return {'data': trace, 'layout': layout}
