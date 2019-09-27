import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
from ConfigFiles import MetricsConfig


def construct_layout(drop_down_income_statement_list):
    metrics = [{'label': str(value), 'value': str(value)} for value in MetricsConfig.main_dictionary["all_metrics"]]
    return [html.Br(),
            dcc.Dropdown(id='drop_down_metrics',
                         options= metrics,
                         multi=True,
                         value=['TOTAL DEBT'],
                         className="dcc_control"),
            html.Br(),

            dcc.RadioItems(id="length_radio",
                           options=[
                               {'label': 'Quarterly', 'value': 'MRQ'},
                               {'label': 'Annually', 'value': 'MRY'}
                           ],
                           value='MRQ',
                           labelStyle={'display': 'inline-block'}
                           ),
            dcc.Loading(
                id="metrics-loading-bar",
                type="circle",
                children=[dcc.Graph(id='financial-metrics-table', figure={'data': [go.Scatter(x=[], y=[])]})])
            ]
