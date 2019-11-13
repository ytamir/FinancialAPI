from PageCallbacks import StockPriceCallbacks, FinancialMetricsCallbacks, MachineLearningCallbacks, StocksInfo


def register_callbacks(app,  cache, cache_timeout, redis_instance, symbols):
    StockPriceCallbacks.register_callbacks(app)
    FinancialMetricsCallbacks.register_callbacks(app, cache, cache_timeout, redis_instance, symbols)
    # MachineLearningCallbacks.register_callbacks(app)
    StocksInfo.register_callbacks(app)
