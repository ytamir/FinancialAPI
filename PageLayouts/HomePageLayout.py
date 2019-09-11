import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html


def construct_layout(drop_down_symbols):
    return [html.Br(),
            dcc.RadioItems(id='home_radio-items',
                           options=[{'label': 'Candlesticks', 'value': 'C'}, {'label': 'Stock Price',
                                                                              'value': 'S'}]),
            html.Br(),
            dcc.Loading(
                id="homepage-loading-bar",
                type="circle",
                children=[dcc.Graph(id='homepage-table', figure={'data': [go.Scatter(x=[], y=[])]})])
            ]

