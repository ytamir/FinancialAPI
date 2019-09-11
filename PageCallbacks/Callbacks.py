from dash.dependencies import Input, Output
from PageCallbacks import HomePageCallbacks, FinancialMetricsCallbacks


def register_callbacks(app, metrics_dict):
    HomePageCallbacks.register_callbacks(app)
    FinancialMetricsCallbacks.register_callbacks(app, metrics_dict)

    @app.callback(Output('symbol', 'children'),
                  [Input('drop_down_symbols', 'value')])
    def set_header(input_symbols):
        my_string = ''
        for symbol in input_symbols:
            my_string = ', '.join(map(str, input_symbols))
        return my_string
