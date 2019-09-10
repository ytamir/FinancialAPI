import dash_core_components as dcc
import plotly.graph_objs as go


def construct_layout():
    return [
        dcc.RadioItems(id='radio-items', options=[{'label': 'Candlesticks', 'value': 'C'}, {'label': 'Stock Price',
                                                                                            'value': 'S'}]),
        dcc.Graph(id='homepage-table', figure={'data': [go.Scatter(x=[], y=[])]})]
