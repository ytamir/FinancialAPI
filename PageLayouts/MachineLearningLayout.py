import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html


def construct_layout(drop_down_symbols):
    return [html.Br(),
            dcc.Dropdown(id='ml_dropdown',
                         options=drop_down_symbols,
                         multi=True,
                         value=['XOM'],
                         className="dcc_control"),
            html.Br(),
            dcc.Loading(
                id="ml-loading-bar",
                type="circle",
                children=[dcc.Graph(id='ml-table', figure={'data': [go.Scatter(x=[], y=[])]})])
            ]
