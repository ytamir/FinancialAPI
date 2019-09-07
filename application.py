import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from PageLayouts import HomePageLayout
from PageCallbacks import Callbacks

init_stock = pd.read_csv("CSVFiles/aapl.csv")
nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")
symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

# Setup the App Layout
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    dcc.Link('Home Page', id="home_page", href='/'),
    html.Br(),
    dcc.Link('Quarterly Page', id="quarterly_page", href='/Quarterly'),
    html.Br(),
    html.Div(id='page-content', children=HomePageLayout.construct_layout(drop_down_symbols, init_stock))
])

# Register All Callbacks Used in the App
Callbacks.register_callbacks(app, init_stock, drop_down_symbols)

if __name__ == '__main__':
    application.run(debug=True, port=8080)
