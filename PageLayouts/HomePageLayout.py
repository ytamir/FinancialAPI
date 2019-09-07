import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


def construct_layout(drop_down_symbols, init_stock):
    return [html.H1(id='symbol', children='AAPL'),
            dcc.Dropdown(id='drop_down_symbols', options=drop_down_symbols, multi=True,
                         className="dcc_control"),
            html.Button(id='submit-button', n_clicks=0, children='Submit'),
            dcc.Graph(id='table', figure={'data': [go.Scatter(x=init_stock['Date'],
                                                              y=init_stock['High'])]})
            ]
