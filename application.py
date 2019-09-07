import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
# from GetStockRowData import StockRowData
import plotly.graph_objs as go
from PyhonRequestFiles.stock import Stocks
from dash.dependencies import Input, Output, State



#df = Stocks.getdata("AAPL")
# df = StockRowData.get_file("GOOGL", SheetType.METRICS, Frequency.QUARTERLY)
# df['Short Date']= pd.to_datetime(df['DATE'])
# df['Short Date'] = df['Short Date'].apply(lambda x:x.date().strftime('%m%d%y'))
# df.to_csv("test.csv", index=False)




#df.to_csv('aapl.csv')
fd = pd.read_csv("CSVFiles/aapl.csv")
dff = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

nasdaqdf = pd.read_csv("CSVFiles/nasdaq.csv")
nysedf = pd.read_csv("CSVFiles/nyse.csv")
symbols = nysedf.Symbol.values.tolist() + nasdaqdf.Symbol.values.tolist()

#print('fd')
#print(fd)



WELL_STATUSES = dict(
    AC = 'Active',
    AR = 'Application Received to Drill/Plug/Convert',
    CA = 'Cancelled',
    DC = 'Drilling Completed',
    DD = 'Drilled Deeper',
    DG = 'Drilling in Progress',
    EX = 'Expired Permit',
    IN = 'Inactive',
    NR = 'Not Reported on AWR',
    PA = 'Plugged and Abandoned',
    PI = 'Permit Issued',
    PB = 'Plugged Back',
    PM = 'Plugged Back Multilateral',
    RE = 'Refunded Fee',
    RW = 'Released - Water Well',
    SI = 'Shut-In',
    TA = 'Temporarily Abandoned',
    TR = 'Transferred Permit',
    UN = 'Unknown',
    UL = 'Unknown Located',
    UM = 'Unknown Not Found',
    VP = 'Voided Permit',
)

well_status_options = [{'label': str(a),
                        'value': str(a)}
                       for a in symbols]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
application = app.server

app.layout = html.Div(children=[
    html.H1(children='AAPL', id='name'),
    dcc.Dropdown(
                            id='well_statuses',
                            options=well_status_options,
                            multi=True,
                            className="dcc_control"
                        ),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),

   dcc.Graph(
    id='table',
    figure = {
        'data': [
            go.Scatter(x=fd['Date'], y=fd['High'])
        ]
        }
)
])




@app.callback([Output('table', 'figure'),
               Output('name','children')],              
              [Input('submit-button', 'n_clicks')],
              [State('well_statuses', 'value')])
def update_output(n_clicks, input_symbols):
    if input_symbols is not None:
        trace = []
        myString = ', '.join(map(str, input_symbols))
        for symbol in input_symbols:
            newdf = Stocks.getdata(symbol)
            print(newdf)
            newdf.to_csv('CSVFiles/test.csv')
            fdd = pd.read_csv("CSVFiles/test.csv")
            #output_name = input_symbol.append(" Stock")
            trace.append(go.Scatter(x=fdd['Date'], y=fdd['High'], name=symbol, mode='lines'))
        return {"data": trace}, myString
    else:
        return {
                   'data': [
                       go.Scatter(x=fd['Date'], y=fd['High'])
                   ]
               }, "AAPL"






# @app.callback(
#     Output('table', 'figure' ),
#     [Input('well_statuses', 'value')]
# )
# def update_graph(input_symbol):
#     if input_symbol in symbols:
#         newdf = Stocks.getdata(input_symbol)
#         newdf.to_csv('test.csv')
#         fdd = pd.read_csv("test.csv")
#         return {
#             'data': [
#                 go.Scatter(x=fd['Date'], y=fdd['High'])
#             ]
#         }

if __name__ == '__main__':
    application.run(debug=True, port=8080)