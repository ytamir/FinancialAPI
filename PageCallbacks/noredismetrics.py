from flask import request, Response
from PyhonRequestFiles import FinancialStatementsJSONParser
import json
from ConfigFiles import MetricsConfig


def make_memoized_key():
    """Method to create cache key for memoized data so we can include request parameters"""
    return request.full_path


def register_callbacks(app, cache, cache_timeout, redis_instance, symbols):
    """
    Used to register the API endpoint of the form "/financialy-metrics?stocks=CERN&metrics=REVENUE&frequency=ANNUAL"
    :param app: Flask App
    :param cache: Flask Cache
    :param cache_timeout: Flask cache timeout set at app level
    :param redis_instance: Redis instance for caching
    :param symbols: List of valid ticker symbols
    """
    @app.route('/financialy-metrics', methods=['GET'])
    def plot_revenue_noredis():
        """Method to handle request for financial data"""
        return_data = []

        # Fetch Data From Parameters
        tickers = request.args.get('stocks', None)
        tickers = tickers.split(";")
        metrics = request.args.get('metrics', None)
        metrics = metrics.split(";")
        quarterly_annual = request.args.get('frequency', None)

        # Validate data before proceeding
        # Check that all request parameters were passed in correctly
        if tickers is None or metrics is None or quarterly_annual is None:
            return Response(json.dumps({'HTTP ERROR 400': 'Not all request parameters specified'}),
                            status=400,
                            mimetype="application/json")
        # Validate Tickers
        for ticker in tickers:
            if ticker not in symbols:
                tickers.remove(ticker)
        if not tickers:
            return Response(json.dumps({'HTTP ERROR 400': 'Ticker Symbols are invalid'}),
                            status=400,
                            mimetype="application/json")
        # Validate Metrics
        for metric in metrics:
            if metric not in MetricsConfig.main_dictionary["all_metrics"]:
                metrics.remove(metric)
        if not metrics:
            return Response(json.dumps({'HTTP ERROR 400': 'Metrics are invalid'}),
                            status=400,
                            mimetype="application/json")
        # Check Frequency
        if quarterly_annual.upper() != "ANNUAL" and quarterly_annual.upper() != "QUARTERLY":
            return Response(json.dumps({'HTTP ERROR 400': 'Frequency must be Quarterly or Annual'}),
                            status=400,
                            mimetype="application/json")

        # Convert from string to int for handling request
        if quarterly_annual.upper() == "ANNUAL":
            quarterly_annual = 1
        elif quarterly_annual.upper() == "QUARTERLY":
            quarterly_annual = 0

        # Make API request with filtered data and symbols
        try:
            stock_data = FinancialStatementsJSONParser.fetch_data(quarterly_annual, metrics, tickers , [])
        except Exception:
            return Response(json.dumps({'HTTP ERROR 400': 'Error fetching data from API'}),
                            status=400,
                            mimetype="application/json")

        for data in stock_data:
            # Install data in redis cache for data we have not cached yet and add data to return
            try:
                return_data.append({"ticker": data["SYMBOL"], "metric": data["METRIC"], "dates": data["DATES"],
                                    "data": data["DATA"]})
            except Exception:
                return Response(json.dumps({'HTTP ERROR 400': 'Error Installing Data in the Cache'}),
                                status=204,
                                mimetype="application/json")

        if not return_data:
            return Response(json.dumps({'HTTP 204': 'No Data Found'}),
                            status=204,
                            mimetype="application/json")
        else:
            return Response(json.dumps({"return_data": return_data}),
                            status=200,
                            mimetype="application/json")

