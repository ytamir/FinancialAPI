import dash_core_components as dcc
import plotly.graph_objs as go


def construct_layout():
    return [dcc.Graph(id='financial-metrics-table', figure={'data': [go.Scatter(x=[],
                                                                                y=[])]})]
