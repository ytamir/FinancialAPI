from flask import Flask
from flask_cors import CORS
import json
import os
from PageCallbacks import Callbacks
import pandas as pd
from pymongo import MongoClient
from redis import Redis

# Read in files
nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")

# Symbols

symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

application  = Flask(__name__)
cache_timeout = 86400 #One Day
redis_instance = Redis(host=os.getenv('REDIS_HOST'), socket_timeout=0.1)
mongo_client = MongoClient("mongodb+srv://"+os.getenv('MONGO_USERNAME')+":"+os.getenv('MONGO_PASSWORD') +
                           "@financialappmongocluster-wdw1z.mongodb.net/test?retryWrites=true&w=majority")
mongo_db = mongo_client['FinancialData']
CORS(application )
Callbacks.register_callbacks(application , cache_timeout, mongo_db, redis_instance, symbols)


@application.route('/get/stock_tickers', methods=['GET','POST'])
def show_post(post_id):
  return json.dumps(drop_down_symbols)

if __name__ == '__main__':
    application .run()

