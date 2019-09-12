import plotly.graph_objs as go
import numpy as np
from PyhonRequestFiles import FinancialMetricsScraper
from dash.dependencies import Input, Output


# TODO transform metrics dropdown to candlestick with selected values

def register_callbacks(app, income_statement_dict, balance_sheet_dict, cash_statement_dict,
                       metrics_statement_dict, drop_down_income_statement_list,
                       drop_down_metrics_statement_list, drop_down_balance_sheet_list,
                       drop_down_cash_statement_list):
    @app.callback(Output('financial-metrics-table', 'figure'),
                  [Input('drop_down_symbols', 'value'),
                   Input('drop_down_metrics', 'value'),
                   Input('type_radio', 'value'),
                   Input('length_radio', 'value')
                   ])
    def plot_revenue(input_symbols, metrics_sel, type_val, length_val):
        trace = []
        this_dict = income_statement_dict
        if type_val == 'Income%20Statement':
            this_dict = income_statement_dict
        elif type_val == 'Cash%20Flow':
            this_dict = cash_statement_dict
        elif type_val == 'Balance%20Sheet':
            this_dict = balance_sheet_dict
        elif type_val == 'Metrics':
            this_dict = metrics_statement_dict

        if input_symbols is not None:
            for symbol in input_symbols:
                color = "rgb" + str(tuple(list(np.random.choice(range(0, 200), size=3))))  # colors will need to change
                # depending on the background color if styles are ever changed
                color_dict = {"color": color}

                for c in metrics_sel:
                    stock_data = FinancialMetricsScraper.StockRowData.get_file(symbol,
                                                                               type_val,
                                                                               length_val)
                    # print("c")
                    # print(c)
                    # print("stock data.head")
                    # print(stock_data.head())
                    # print("metrics_dict[str(c)]")
                    # print(metrics_dict[str(c)])

                    trace.append(go.Scatter(x=stock_data.iloc[:, 0], y=stock_data.iloc[:, c],
                                            name=symbol + ": " + this_dict[str(c)],
                                            mode='lines+markers', line=color_dict))
        return {"data": trace}

    # could make 4 seperate drop down and hide 3 each time so that the values are saved
    @app.callback(Output('drop_down_metrics', 'options'),
                  [Input('type_radio', 'value')])
    def update_category_drop_down(type_val):
        if type_val == 'Income%20Statement':
            return drop_down_income_statement_list
        elif type_val == 'Cash%20Flow':
            return drop_down_cash_statement_list
        elif type_val == 'Balance%20Sheet':
            return drop_down_balance_sheet_list
        elif type_val == 'Metrics':
            return drop_down_metrics_statement_list

    @app.callback(Output('drop_down_metrics', 'value'),
                  [Input('type_radio', 'value')])
    def update_category_drop_down(type_val):
        return [1]
