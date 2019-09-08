import dash_core_components as dcc
import plotly.graph_objs as go


def construct_layout(init_stock):
    return [dcc.Graph(id='financial-metrics-table', figure={'data': [go.Scatter(x=init_stock['Date'],
                                                                                y=init_stock['High'])]})]
