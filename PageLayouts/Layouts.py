import dash_core_components as dcc
import dash_html_components as html
from PageLayouts import HomePageLayout, FinancialMetricsPageLayout


def construct_layout(drop_down_symbols, drop_down_metrics_list):
    return [
        dcc.Location(id='url', refresh=False),

        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
            dcc.Tab(label='Home Page', value='tab-1-example',
                    children=HomePageLayout.construct_layout(drop_down_symbols)),
            dcc.Tab(label='Financial Metrics Page', value='tab-2-example',
                    children=FinancialMetricsPageLayout.construct_layout(drop_down_symbols, drop_down_metrics_list))
        ]),
        # This is a hidden state for our stocks we have currently selected, that I figured might be useful
        html.Div(id='stock_state', style={'display': 'none'})
    ]
