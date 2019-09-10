import dash_core_components as dcc
import plotly.graph_objs as go


def construct_layout(drop_down_metrics_list):
    return [
        dcc.Dropdown(id='metrics_drop_down', options=drop_down_metrics_list, multi=True, value=[1],
                     className="dcc_control"),
        dcc.Graph(id='financial-metrics-table', figure={'data': [go.Scatter(x=[],
                                                                            y=[])]})]
