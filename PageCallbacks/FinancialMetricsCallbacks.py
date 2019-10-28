import plotly.graph_objs as go
from PyhonRequestFiles import FinancialStatementsJSONParser
from dash.dependencies import Input, Output
import numpy as np


def register_callbacks(app, cache, cache_timeout, redis_instance):

    @app.route('/financial_metrics/<tickers>')
    @cache.memoize(timeout=cache_timeout)  # in seconds
    #def plot_revenue(stocks, metrics, quarterly_annual):
    def plot_revenue(stocks, metrics, quarterly_annual):
        trace = []
        color_dict = {}

        # COLORS
        for stock in stocks:
            color_dict.update({stock: {"color": "rgb" + str(
                tuple(list(np.random.choice(range(0, 200), size=3))))}})

        # Retrieved cached data and append it to our return value
        for index, metric in enumerate(metrics):
            for stock in stocks:
                dates_data = get_cached_data(stock, metric, quarterly_annual, redis_instance)

                if dates_data[0] and dates_data[1]:
                    # print("Using Old Data For " + stock + " " + metric + ".")
                    # print(dates_data[1])
                    trace.append(
                        go.Scatter(x=dates_data[0], y=dates_data[1], name=stock + ": " + metric,
                                   mode='lines+markers', line=color_dict[stock]))

        # Get a list of symbols we can ignore for different metrics because of cached data
        symbols_to_ignore_for_metric = construct_symbols_to_ignore(stocks, metrics, quarterly_annual)

        # Filter metrics so we don't request data we do not need because of cached data
        filtered_metrics = [i for j, i in enumerate(metrics) if j not in indices_to_remove(metrics, stocks,
                                                                                           quarterly_annual,
                                                                                           remove_stocks=False)]
        # Filter stocks so we don't request data we do not need because of cached data
        filtered_stocks = [i for j, i in enumerate(stocks) if j not in indices_to_remove(stocks, metrics,
                                                                                         quarterly_annual,
                                                                                         remove_stocks=True)]
        # Make API request with filtered data and symbols
        stock_data = FinancialStatementsJSONParser.fetch_data(quarterly_annual, filtered_metrics, filtered_stocks,
                                                              symbols_to_ignore_for_metric)
        for data in stock_data:
            # Install data in redis cache for data we have not cached yet
            cache_data(data, quarterly_annual, cache_timeout, redis_instance)
            # print("USING NEW DATA FOR " + data["SYMBOL"] + " " + data["METRIC"] + ".")
            # print(data["DATA"])

            # Add data to return
            trace.append(go.Scatter(x=data["DATES"], y=data["DATA"], name=data["SYMBOL"] + ": " + data["METRIC"],
                                    mode='lines+markers', line=color_dict[data["SYMBOL"]]))
        # Return our plots
        return {"data": trace}

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
