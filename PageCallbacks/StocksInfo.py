


#!/usr/bin/env python
from urllib.request import urlopen
import json



def register_callbacks(app):    
    @app.route('/get/companyprofile/<ticker>', methods=['GET'])
    def get_stock_data(ticker):
        url = ("https://financialmodelingprep.com/api/company/profile/" + ticker.upper() +"?datatype=json")
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.dumps(data)

    @app.route('/get/companyprofile/<ticker>', methods=['GET'])
    def get_stocks_data():
        url = ("https://financialmodelingprep.com/api/stock/list/all?datatype=json")
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)
    
