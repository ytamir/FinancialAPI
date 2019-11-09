from flask import request, Response
from PyhonRequestFiles import FinancialStatementsJSONParser
import json
import MetricsConfig


def make_memoized_key():
    """Method to create cache key for memoized data so we can include request parameters"""
    return request.full_path


def register_callbacks(app, cache, cache_timeout, redis_instance, symbols):
    """
    Used to register the API endpoint of the form "/financial-metrics?stocks=CERN&metrics=REVENUE&frequency=ANNUAL"
    :param app: Flask App
    :param cache: Flask Cache
    :param cache_timeout: Flask cache timeout set at app level
    :param redis_instance: Redis instance for caching
    :param symbols: List of valid ticker symbols
    """
    @app.route('/financial-metrics', methods=['GET'])
    @cache.cached(timeout=cache_timeout, key_prefix=make_memoized_key)
    def plot_revenue():
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

        # Retrieved cached data and append it to our return value
        try:
            for index, metric in enumerate(metrics):
                for stock in tickers:
                    dates_data = get_cached_data(stock, metric, quarterly_annual, redis_instance)
                    if dates_data[0] and dates_data[1]:
                        return_data.append({"ticker": stock, "metric": metric, "dates": dates_data[0],
                                            "data": dates_data[1]})
        except Exception:
            return Response(json.dumps({'HTTP ERROR 400': 'Error fetching cached data'}),
                            status=400,
                            mimetype="application/json")

        # Get a list of symbols and metrics we can ignore for different metrics because of cached data
        try:
            symbols_to_ignore_for_metric = construct_symbols_to_ignore(tickers, metrics, quarterly_annual)
            filtered_metrics = [i for j, i in enumerate(metrics) if j not in indices_to_remove(metrics, tickers,
                                                                                               quarterly_annual,
                                                                                               remove_stocks=False)]
            filtered_stocks = [i for j, i in enumerate(tickers) if j not in indices_to_remove(tickers, metrics,
                                                                                              quarterly_annual,
                                                                                              remove_stocks=True)]
        except Exception:
            return Response(json.dumps({'HTTP ERROR 400': 'Error filtering stock symbols and metrics'}),
                            status=400,
                            mimetype="application/json")

        # Make API request with filtered data and symbols
        try:
            stock_data = FinancialStatementsJSONParser.fetch_data(quarterly_annual, filtered_metrics, filtered_stocks,
                                                                  symbols_to_ignore_for_metric)
        except Exception:
            return Response(json.dumps({'HTTP ERROR 400': 'Error fetching data from API'}),
                            status=400,
                            mimetype="application/json")

        for data in stock_data:
            # Install data in redis cache for data we have not cached yet and add data to return
            try:

                cache_data(data, quarterly_annual, cache_timeout, redis_instance)
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

    def cache_data(data, quarterly_or_annual, cache_expire, redis_connection):
        """
        Caches data array and dates array from API into redis
        :param cache_expire: How long data will stay in redis
        :param data: Contains data to cache
        :param quarterly_or_annual: Whether data is quarterly or annual
        :param redis_connection: Redis connection for caching
        """
        for data_item, date_item in zip(data["DATA"], data["DATES"]):
            data_key = construct_key(data["SYMBOL"], data["METRIC"], quarterly_or_annual, key_type_data=True)
            dates_key = construct_key(data["SYMBOL"], data["METRIC"], quarterly_or_annual, key_type_data=False)
            redis_connection.lpush(dates_key, date_item)
            redis_connection.expire(name=dates_key, time=cache_expire)
            redis_connection.lpush(data_key, data_item)
            redis_connection.expire(name=data_key, time=cache_expire)

    def construct_symbols_to_ignore(stocks, metrics, quarterly_or_annual):
        """
        Returns a list of stocks to ignore for a specified metric of the form
        [metric1-stock1, metric1-stock2, metric2-stock1, ... ]
        :param stocks: All stocks requested
        :param metrics: All metrics request
        :param quarterly_or_annual: Data is quarterly or annual
        """
        symbols_to_ignore_for_metric = []
        for index, metric in enumerate(metrics):
            for stock in stocks:
                data_key = construct_key(stock, metric, quarterly_or_annual, key_type_data=True)
                dates_key = construct_key(stock, metric, quarterly_or_annual, key_type_data=False)
                # If both keys exist, we have the cached data
                if redis_instance.exists(dates_key) and redis_instance.exists(data_key):
                    symbols_to_ignore_for_metric.append(metric + "-" + stock)

        return symbols_to_ignore_for_metric

    def construct_key(stock, metric, quarterly_or_annual, key_type_data):
        """
        Construct a redis dates or data key for the given parameters
        :param stock: Stock
        :param metric:  Financial Metric
        :param quarterly_or_annual: Whether data is quarterly or annual
        :param key_type_data: Two Types of keys either date key or data key
        :return: Constructed redis key for either dates or data
        """
        quarterly_annual_string = "Annualy" if quarterly_or_annual else "Quarterly"
        key = stock + "-" + metric + "-" + quarterly_annual_string + "-" + "Data" if key_type_data \
            else stock + "-" + metric + "-" + quarterly_annual_string + "-" + "Dates"
        return key

    def get_cached_data(stock, metric, quarterly_or_annual, redis_connection):
        dates_list = []
        data_list = []
        data_key = construct_key(stock, metric, quarterly_or_annual, key_type_data=True)
        dates_key = construct_key(stock, metric, quarterly_or_annual, key_type_data=False)
        if redis_connection.exists(dates_key) and redis_connection.exists(data_key):
            dates_list = [x.decode('utf-8') for x in redis_connection.lrange(dates_key, 0, -1)]
            data_list = [x.decode('utf-8') for x in redis_connection.lrange(data_key, 0, -1)]
        return [dates_list, data_list]

    def indices_to_remove(list1, list2, quarterly_or_annual, remove_stocks):
        """
        This method checks if any of the requested symbols or metrics can be removed from our API request if we already
        have the cached data
        :param list1: Could be list of all symbols or list of all metrics
        :param list2: Could be list of all symbols or list of all metrics
        :param quarterly_or_annual: Is the data quarterly or annul
        :param remove_stocks: If true we are filtering stock list, otherwise filtering the metrics list
        """
        remove_indices = []
        for index, value1 in enumerate(list1):
            remove = True
            for value2 in list2:
                if remove_stocks:
                    data_key = construct_key(value1, value2, quarterly_or_annual, key_type_data=True)
                    dates_key = construct_key(value1, value2, quarterly_or_annual, key_type_data=False)
                else:
                    data_key = construct_key(value2, value1, quarterly_or_annual, key_type_data=True)
                    dates_key = construct_key(value2, value1, quarterly_or_annual, key_type_data=False)

                # If the data does not exist for  some key we cannot remove anything
                if not redis_instance.exists(dates_key) or not redis_instance.exists(data_key):
                    remove = False
                    break
            if remove:
                remove_indices.append(index)
        return remove_indices
