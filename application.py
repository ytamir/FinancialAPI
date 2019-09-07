import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from PyhonRequestFiles.stock import Stocks
from dash.dependencies import Input, Output, State

init_stock = pd.read_csv("CSVFiles/aapl.csv")

nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")
symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

app.layout = html.Div(children=[
    html.H1(children='AAPL', id='symbol'),
    dcc.Dropdown(id='drop_down_symbols', options=drop_down_symbols, multi=True, className="dcc_control"),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    dcc.Graph(id='table', figure={'data': [go.Scatter(x=init_stock['Date'], y=init_stock['High'])]})
])


@app.callback([Output('table', 'figure'),
               Output('symbol', 'children')],
              [Input('submit-button', 'n_clicks')],
              [State('drop_down_symbols', 'value')])
def update_output(n_clicks, input_symbols):
    if input_symbols is not None:
        trace = []
        for symbol in input_symbols:
            stock_data = Stocks.getdata(symbol)
            stock_data.to_csv('CSVFiles/test.csv')
            stock_data_out = pd.read_csv("CSVFiles/test.csv")
            trace.append(go.Scatter(x=stock_data_out['Date'], y=stock_data_out['High'], name=symbol, mode='lines'))
        my_string = ', '.join(map(str, input_symbols))
        return {"data": trace}, my_string
    else:
        return {
                   'data': [
                       go.Scatter(x=init_stock['Date'], y=init_stock['High'])
                   ]
               }, "AAPL"


if __name__ == '__main__':
    application.run(debug=True, port=8080)
