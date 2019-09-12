import dash
import dash_html_components as html
import pandas as pd

from ConfigFiles import Config
from PageLayouts import Layouts
from PageCallbacks import Callbacks

# Read in files
nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")
metrics = pd.read_csv("CSVFiles/metrics.csv")

# Homepage setup
symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

# Setup Financial Metrics Page
count = 0
income_statement_dict = {str(count): "Date"}
balance_sheet_dict = {str(count): "Date"}
cash_statement_dict = {str(count): "Date"}
metrics_statement_dict = {str(count): "Date"}

drop_down_income_statement_list = []
drop_down_metrics_statement_list = []
drop_down_balance_sheet_list = []
drop_down_cash_statement_list = []

for metric in Config.income_statement_metrics:
    drop_down_income_statement_list.append({'label': metric, 'value': count})
    income_statement_dict[str(count)] = metric
    count += 1
count = 0
for metric in Config.balance_sheet_metrics:
    drop_down_balance_sheet_list.append({'label': metric, 'value': count})
    balance_sheet_dict[str(count)] = metric
    count += 1
count = 0
for metric in Config.cash_statement_metrics:
    drop_down_cash_statement_list.append({'label': metric, 'value': count})
    cash_statement_dict[str(count)] = metric
    count += 1
count = 0
for metric in Config.metrics_statement_metrics:
    drop_down_metrics_statement_list.append({'label': metric, 'value': count})
    metrics_statement_dict[str(count)] = metric
    count += 1

# Setup site
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

# Setup the App Layout
app.layout = html.Div(children=Layouts.construct_layout(drop_down_symbols,drop_down_income_statement_list))
# Register Callbacks
Callbacks.register_callbacks(app, income_statement_dict, balance_sheet_dict, cash_statement_dict,
                             metrics_statement_dict, drop_down_income_statement_list,
                             drop_down_metrics_statement_list, drop_down_balance_sheet_list,
                             drop_down_cash_statement_list)

if __name__ == '__main__':
    application.run(debug=True, port=8080)
