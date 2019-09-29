import dash
import dash_html_components as html
import pandas as pd
from PageLayouts import Layouts
from PageCallbacks import Callbacks

# Read in files
nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")

# Homepage setup
symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

# Setup site
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

# Setup the App Layout
app.layout = html.Div(children=Layouts.construct_layout(drop_down_symbols))
# Register Callbacks
Callbacks.register_callbacks(app)

if __name__ == '__main__':
    application.run(debug=True, port=80)
