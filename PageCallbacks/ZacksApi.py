from flask import request, Response
from PyhonRequestFiles import ZacksScraper
import json


def register_api(app):

    @app.route('/etf-holdings', methods=['GET'])
    def holding_endpoint():
        """
        This function takes in a ticker symbol from the Url and returns the json formatted holding data or an error
        :return: Either HTTP Status Code Error or Holding Data in Json Format
                 JSON Format "Holdings : { Holding 1: [ shares, %portfolio, 52week changed ], ... }"
        """

        ticker = request.args.get('ticker', None)
        if ticker is None:
            return Response(json.dumps({'HTTP ERROR 400': 'Not all request parameters specified'}),
                            status=400,
                            mimetype="application/json")
        else:
            # TODO Add More Validation and check whether the ticker is ETF or Mutual Fund
            return Response(json.dumps(ZacksScraper.scrape_holdings(ticker, True)),
                            status=200,
                            mimetype="application/json")
