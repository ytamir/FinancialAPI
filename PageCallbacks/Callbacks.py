from dash.dependencies import Input, Output
from PageCallbacks import HomePageCallbacks, FinancialMetricsCallbacks


def register_callbacks(app):
    HomePageCallbacks.register_callbacks(app)
    FinancialMetricsCallbacks.register_callbacks(app)
