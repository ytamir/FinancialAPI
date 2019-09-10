import plotly.graph_objs as go
from PyhonRequestFiles import FinancialMetricsScraper
from dash.dependencies import Input, Output, State


def register_callbacks(app):
    @app.callback(Output('financial-metrics-table', 'figure'),
                  [Input('drop_down_symbols', 'value')])
    def plot_revenue(input_symbols):
        trace = []
        if input_symbols is not None:

            for symbol in input_symbols:
                stock_data = FinancialMetricsScraper.StockRowData.get_file(symbol,
                                                                           FinancialMetricsScraper.SheetType.
                                                                           INCOME_STATEMENT,
                                                                           FinancialMetricsScraper.Frequency.QUARTERLY)

                trace.append(go.Scatter(x=stock_data.iloc[:, 0], y=stock_data.iloc[:, 1], name=symbol, mode='lines'))
        return {"data": trace}
