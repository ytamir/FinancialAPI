import plotly.graph_objs as go
from PyhonRequestFiles import FinancialStatementsJSONParser
from dash.dependencies import Input, Output


def register_callbacks(app):
    @app.callback(Output('financial-metrics-table', 'figure'),
                  [Input('drop_down_symbols', 'value'),
                   Input('drop_down_metrics', 'value'),
                   Input('length_radio', 'value')
                   ])
    def plot_revenue(stocks, metrics, quarterly_annual):
        trace = []
        stock_data = FinancialStatementsJSONParser.fetch_data(quarterly_annual, metrics, stocks)
        for data in stock_data:
            trace.append(go.Scatter(x=data["DATES"], y=data["DATA"], name=data["SYMBOL"]))
        return {"data": trace}
