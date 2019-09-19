import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html


def construct_layout(drop_down_symbols):
    return [html.Br(),
            dcc.RadioItems(id='home_radio-items',
                           options=[{'label': 'Stock Price',
                                     'value': 'S'}, {'label': 'Candlesticks', 'value': 'C'}], value='S',
                           labelStyle={'display': 'inline-block'}),
            dcc.RadioItems(id='time_radio-items',
                           options=[{'label': 'Daily',
                                     'value': 'd'}, {'label': 'Intra-day', 'value': 'i'}], value='d',
                           labelStyle={'display': 'inline-block'}),
            html.Br(),
            dcc.Loading(
                id="homepage-loading-bar",
                type="circle",
                children=[dcc.Graph(id='homepage-table', figure={'data': [go.Scatter(x=[], y=[])]})])
            ]
