from dash.dependencies import Input, Output
from PageCallbacks import HomePageCallbacks, FinancialMetricsCallbacks, MachineLearningCallbacks


def register_callbacks(app):
    HomePageCallbacks.register_callbacks(app)
    FinancialMetricsCallbacks.register_callbacks(app)
    MachineLearningCallbacks.register_callbacks(app)
