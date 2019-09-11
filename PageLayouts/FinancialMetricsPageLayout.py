import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html


def construct_layout(drop_down_symbols, drop_down_metrics_list):
    return [html.H1(id='symbol', children='AAPL'),
            dcc.Dropdown(id='drop_down_symbols', options=drop_down_symbols, multi=True,
                         className="dcc_control", value=["AAPL"]),
            dcc.Dropdown(id='metrics_drop_down', options=drop_down_metrics_list, multi=True, value=[1],
                         className="dcc_control"),
            dcc.Loading(
                id="metrics-loading-bar",
                type="circle",
                children=[dcc.Graph(id='financial-metrics-table', figure={'data': [go.Scatter(x=[], y=[])]})])
            ]

