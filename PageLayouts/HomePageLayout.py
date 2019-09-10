import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html


def construct_layout(drop_down_symbols):
    return [html.H1(id='home_symbol', children='AAPL'),
            dcc.Dropdown(id='home_drop_down_symbols', options=drop_down_symbols, multi=True,
                         className="dcc_control", value=["AAPL"]),
            dcc.RadioItems(id='home_radio-items',
                           options=[{'label': 'Candlesticks', 'value': 'C'}, {'label': 'Stock Price',
                                                                              'value': 'S'}]),
            dcc.Graph(id='homepage-table', figure={'data': [go.Scatter(x=[], y=[])]})]
