import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html


def construct_layout(drop_down_symbols, drop_down_metrics_list):
    return [html.Br(),
            dcc.Dropdown(id='metrics_drop_down', options=drop_down_metrics_list, multi=True, value=[1],
                         className="dcc_control"),
            html.Br(),
            dcc.Loading(
                id="metrics-loading-bar",
                type="circle",
                children=[dcc.Graph(id='financial-metrics-table', figure={'data': [go.Scatter(x=[], y=[])]})])
            ]

