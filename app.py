from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
import json
import os
from PageCallbacks import Callbacks
import pandas as pd
from redis import Redis

# Read in files
nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")

# Symbols
symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST': 'ec2-18-218-166-157.us-east-2.compute.amazonaws.com'
 })
cache_timeout = 3600
redis_instance = Redis(host='ec2-18-218-166-157.us-east-2.compute.amazonaws.com')
CORS(app)
Callbacks.register_callbacks(app, cache, cache_timeout, redis_instance, symbols)

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
