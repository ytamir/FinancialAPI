import dash_core_components as dcc
import dash_html_components as html
from PageLayouts import HomePageLayout, FinancialMetricsPageLayout


def construct_layout(drop_down_symbols, drop_down_metrics_list):
    return [
        dcc.Location(id='url', refresh=False),
        dcc.Link('Home Page', id="home_page", href='/'),
        html.Br(),
        dcc.Link('Financial Metrics Page', id="financial_metrics_page", href='/FinancialMetrics'),
        html.Br(),

        html.H1(id='symbol', children='AAPL'),
        dcc.Dropdown(id='drop_down_symbols', options=drop_down_symbols, multi=True,
                     className="dcc_control", value=["AAPL"]),

        # This is the layout for our page links, on initial load, everything but the home page is hidden
        dcc.Loading(
            id="loading_bar",
            type="circle",
            children=[html.Div(id='home-page-content', children=HomePageLayout.construct_layout()),
                      html.Div(id='financial-metrics-page-content',
                               children=FinancialMetricsPageLayout.construct_layout(drop_down_metrics_list),
                               style={'display': 'none'})]
        ),


        # This is a hidden state for our stocks we have currently selected, that I figured might be useful
        html.Div(id='stock_state', style={'display': 'none'})
    ]