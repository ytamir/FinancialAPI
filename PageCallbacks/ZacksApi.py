from flask import request, Response
from PyhonRequestFiles import ZacksScraper
import json


def register_api(app):

    @app.route('/etf-holdings', methods=['GET'])
    def holding_endpoint():
        """
        This function takes in a ticker symbol from the Url and returns the json formatted holding data or an error
        :return: Either HTTP Status Code Error or Holding Data in Json Format
        """

        ticker = request.args.get('ticker', None)
        if ticker is None:
            return Response(json.dumps({'HTTP ERROR 400': 'Not all request parameters specified'}, indent=4,
                                       sort_keys=True), status=400)
        else:
            try:
                success_json = ZacksScraper.scrape_etf_holdings(ticker)
                return Response(success_json, status=200)
            except:
                return Response(json.dumps({'HTTP ERROR 404': 'Error Fetching ETF Data'}, indent=4, sort_keys=True),
                                status=404)
