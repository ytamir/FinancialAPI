import dash
import dash_html_components as html
import pandas as pd

from PageLayouts import Layouts
from PageCallbacks import Callbacks

# Read in files
nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")
metrics = pd.read_csv("CSVFiles/metrics.csv")

# Homepage setup
symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

# Setup Quarterly Page
metrics_dict = {"0": "Date"}
drop_down_metrics_list = []
for count, col in enumerate(metrics.columns, start=1):
    drop_down_metrics_list.append({'label': str(col), 'value': count})
    metrics_dict[str(count)] = str(col)
    count += 1

# Setup site
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

# Setup the App Layout
app.layout = html.Div(children=Layouts.construct_layout(drop_down_symbols, drop_down_metrics_list))
# Register Callbacks
Callbacks.register_callbacks(app, metrics_dict)

if __name__ == '__main__':
    application.run(debug=True, port=8080)
