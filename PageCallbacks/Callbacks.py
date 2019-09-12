from dash.dependencies import Input, Output
from PageCallbacks import HomePageCallbacks, FinancialMetricsCallbacks


def register_callbacks(app, income_statement_dict, balance_sheet_dict, cash_statement_dict,
                       metrics_statement_dict, drop_down_income_statement_list,
                       drop_down_metrics_statement_list, drop_down_balance_sheet_list,
                       drop_down_cash_statement_list):
    HomePageCallbacks.register_callbacks(app)
    FinancialMetricsCallbacks.register_callbacks(app, income_statement_dict, balance_sheet_dict, cash_statement_dict,
                                                 metrics_statement_dict, drop_down_income_statement_list,
                                                 drop_down_metrics_statement_list, drop_down_balance_sheet_list,
                                                 drop_down_cash_statement_list)

    @app.callback(Output('symbol', 'children'),
                  [Input('drop_down_symbols', 'value')])
    def set_header(input_symbols):
        my_string = ''
        for symbol in input_symbols:
            my_string = ', '.join(map(str, input_symbols))
        return my_string
