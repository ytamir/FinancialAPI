import dash
from PageCallbacks import HomePageCallbacks, FinancialMetricsCallbacks


def register_callbacks(app, init_stock):

    # Callbacks for App Control
    @app.callback([dash.dependencies.Output('home-page-content', 'style'),
                   dash.dependencies.Output('financial-metrics-page-content', 'style'),
                   dash.dependencies.Output('stock_state', 'children')],
                  [dash.dependencies.Input('url', 'pathname'),
                   dash.dependencies.Input('drop_down_symbols', 'value')])
    def page_control(pathname, input_symbols):
        if pathname == "/FinancialMetrics":
            return {'display': 'none'}, {}, input_symbols
        else:
            return {}, {'display': 'none'}, input_symbols

    HomePageCallbacks.register_callbacks(app, init_stock)
    FinancialMetricsCallbacks.register_callbacks(app, init_stock)
