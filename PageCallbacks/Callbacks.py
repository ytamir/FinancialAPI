from PageCallbacks import StockPriceCallbacks, FinancialMetricsCallbacks, MachineLearningCallbacks, StocksInfo, noredismetrics
from PageCallbacks import ZacksApi

def register_callbacks(app,  cache, cache_timeout, redis_instance, symbols):
    StockPriceCallbacks.register_callbacks(app)
    FinancialMetricsCallbacks.register_callbacks(app, cache, cache_timeout, redis_instance, symbols)
    noredismetrics.register_callbacks(app, cache, cache_timeout, redis_instance, symbols)
    ZacksApi.register_api(app)
    # MachineLearningCallbacks.register_callbacks(app)
    StocksInfo.register_callbacks(app)
