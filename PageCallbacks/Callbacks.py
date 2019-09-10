import dash
from PageCallbacks import HomePageCallbacks, FinancialMetricsCallbacks


def register_callbacks(app, metrics_dict):
    HomePageCallbacks.register_callbacks(app)
    FinancialMetricsCallbacks.register_callbacks(app, metrics_dict)
