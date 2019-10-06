import dash_core_components as dcc
import dash_html_components as html
from PageLayouts import HomePageLayout, FinancialMetricsPageLayout, MachineLearningLayout


def construct_layout(drop_down_symbols):
    return [
        dcc.Location(id='url', refresh=False),
        dcc.Dropdown(id='drop_down_symbols', options=drop_down_symbols, multi=True,
                     className="dcc_control", value=["XOM"]),
        html.Br(),
        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
            dcc.Tab(label='Price Analysis', value='tab-1-example',
                    children=HomePageLayout.construct_layout(drop_down_symbols)),
            dcc.Tab(label='Financial Metrics', value='tab-2-example',
                    children=FinancialMetricsPageLayout.construct_layout()),
            dcc.Tab(label='Machine Learning', value='tab-3-example',
                    children=MachineLearningLayout.construct_layout(drop_down_symbols))
        ]),
        # This is a hidden state for our stocks we have currently selected, that I figured might be useful
        html.Div(id='stock_state', style={'display': 'none'})
    ]
