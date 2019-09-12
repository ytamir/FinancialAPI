import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html


def construct_layout(drop_down_income_statement_list):
    return [html.Br(),
            dcc.Dropdown(id='drop_down_metrics', options=drop_down_income_statement_list, multi=True,
                         value=[1],
                         className="dcc_control"),
            html.Br(),
            dcc.RadioItems(id="type_radio",
                           options=[
                               {'label': 'Income Statement', 'value': 'Income%20Statement'},
                               {'label': 'Cash Flow Statement', 'value': 'Cash%20Flow'},
                               {'label': 'Balance Sheet', 'value': 'Balance%20Sheet'},
                               {'label': 'Metrics', 'value': 'Metrics'}
                           ],
                           value='Income%20Statement',
                           labelStyle={'display': 'inline-block'}
                           ),

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
