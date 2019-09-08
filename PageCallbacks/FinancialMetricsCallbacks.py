import plotly.graph_objs as go
from PyhonRequestFiles import FinancialMetricsScraper
from dash.dependencies import Input, Output, State


def register_callbacks(app, init_stock):
    @app.callback(Output('financial-metrics-table', 'figure'),
                  [Input('submit-button', 'n_clicks')],
                  [State('drop_down_symbols', 'value')])
    def plot_revenue(n_clicks, input_symbols):
        if input_symbols is not None:
            print(input_symbols)
            trace = []
            for symbol in input_symbols:
                stock_data = FinancialMetricsScraper.StockRowData.get_file(symbol,
                                                                           FinancialMetricsScraper.SheetType.
                                                                           INCOME_STATEMENT,
                                                                           FinancialMetricsScraper.Frequency.QUARTERLY)
                print(symbol)
                print(stock_data)
                trace.append(go.Scatter(x=stock_data.iloc[:, 0], y=stock_data.iloc[:, 1], name=symbol, mode='lines'))
            return {"data": trace}
        else:
            return {'data': [go.Scatter(x=init_stock['Date'], y=init_stock['High'])]}
