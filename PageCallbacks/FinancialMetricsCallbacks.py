import plotly.graph_objs as go
from PyhonRequestFiles import FinancialMetricsScraper
from dash.dependencies import Input, Output


# TODO transform metrics dropdown to candlestick with selected values

def register_callbacks(app, metrics_dict):
    @app.callback(Output('financial-metrics-table', 'figure'),
                  [Input('drop_down_symbols', 'value'),
                   Input('metrics_drop_down', 'value')])
    def plot_revenue(input_symbols, metrics_sel):
        trace = []
        if input_symbols is not None:
            for symbol in input_symbols:
                for c in metrics_sel:
                    stock_data = FinancialMetricsScraper.StockRowData.get_file(symbol,
                                                                               FinancialMetricsScraper.SheetType.
                                                                               INCOME_STATEMENT,
                                                                               FinancialMetricsScraper.Frequency.QUARTERLY)
                    # print("c")
                    # print(c)
                    # print("stock data.head")
                    # print(stock_data.head())
                    # print("metrics_dict[str(c)]")
                    # print(metrics_dict[str(c)])
                    trace.append(go.Scatter(x=stock_data.iloc[:, 0], y=stock_data.iloc[:, c], name=symbol + ": " + metrics_dict[str(c)],
                                            mode='lines'))
        return {"data": trace}
