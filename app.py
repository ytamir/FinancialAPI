from flask import Flask, request
from flask_cors import CORS
import json
import dash
import dash_html_components as html
from flask_caching import Cache
import os
from PageLayouts import Layouts
from PageCallbacks import Callbacks
import pandas as pd
from redis import Redis
from flask import Flask
from PageCallbacks import StockPriceCallbacks, FinancialMetricsCallbacks, MachineLearningCallbacks





# Read in files
nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")

# Homepage setup
symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

app = Flask(__name__)
CORS(app)

Callbacks.register_callbacks(app) # , cache, cache_timeout, redis_instance

@app.route('/')
def index():
  return 'Index Page'

@app.route('/hello')
def hello():
  return 'Hello, greetings from different endpoint'

#adding variables
@app.route('/user/<username>')
def show_user(username):
  #returns the username
  return 'Username: %s' % username

@app.route('/get/stock_tickers', methods=['GET','POST'])
def show_post(post_id):
  return json.dumps(drop_down_symbols)
