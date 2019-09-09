import dash_core_components as dcc
import plotly.graph_objs as go


def construct_layout(init_revenue):
    return [dcc.Graph(id='financial-metrics-table', figure={'data': [go.Scatter(x=init_revenue.iloc[:, 0],
                                                                                y=init_revenue.iloc[:, 1])]})]
