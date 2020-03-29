from flask import Flask
from flask_cors import CORS
import json
import os
import logging
from logging.handlers import RotatingFileHandler
from PageCallbacks import Callbacks
import pandas as pd
from pymongo import MongoClient
from redis import Redis
import stat

# Read in files
nasdaq = pd.read_csv("CSVFiles/nasdaq.csv")
nyse = pd.read_csv("CSVFiles/nyse.csv")

# Symbols
symbols = nyse.Symbol.values.tolist() + nasdaq.Symbol.values.tolist()
drop_down_symbols = [{'label': str(a), 'value': str(a)} for a in symbols]

# Create Application
application  = Flask(__name__)

# Setup Logging
logger = None
try:
    if os.path.exists("/opt/python/log/application.log"):
        logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024, backupCount=5)
        handler.setFormatter(formatter)
        application.logger.addHandler(handler)
except Exception:
    pass

# Setup Cache Timeout - One Day in Seconds
cache_timeout = 86400

# Setup Redis
redis_isntance = None
try:
    redis_instance = Redis(host=os.getenv('REDIS_HOST'), socket_timeout=0.1)
except Exception:
    if logger is not None:
        logger.debug("Redis could not be configured!")
    pass

# Setup Mongo
mongo_db = None
try:
    mongo_client = MongoClient("mongodb+srv://" + os.getenv('MONGO_USERNAME') + ":" + os.getenv('MONGO_PASSWORD') +
                                "@financialappmongocluster-wdw1z.mongodb.net/test?retryWrites=true&w=majority",
                                 serverSelectionTimeoutMS = 500)
    mongo_db = mongo_client['FinancialData']
except Exception:
    if logger is not None:
        logger.debug("Mongo could not be configured!")
    pass

#Setup Cors - Not Sure if we need this
CORS( application )

# Register Callbackss
Callbacks.register_callbacks(application , cache_timeout, mongo_db, logger, redis_instance, symbols)

@application.route('/get/stock_tickers', methods=['GET','POST'])
def show_post(post_id):
  return json.dumps(drop_down_symbols)

if __name__ == '__main__':
    application .run()

