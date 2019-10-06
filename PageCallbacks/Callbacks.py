from PageCallbacks import HomePageCallbacks, FinancialMetricsCallbacks, MachineLearningCallbacks


def register_callbacks(app, cache, cache_timeout, redis_instance):
    HomePageCallbacks.register_callbacks(app)
    FinancialMetricsCallbacks.register_callbacks(app, cache, cache_timeout, redis_instance)
    MachineLearningCallbacks.register_callbacks(app)
