import dash
from PageCallbacks import HomePageCallbacks
from PageLayouts import HomePage, QuarterlyPage


def register_callbacks(app, init_stock, drop_down_symbols):

    # Callbacks for App Control
    @app.callback(dash.dependencies.Output('page-content', 'children'),
                  [dash.dependencies.Input('url', 'pathname')])
    def page_control(pathname):
        print(pathname)
        if pathname == "/Quarterly":
            return QuarterlyPage.construct_layout()
        else:
            return HomePage.construct_layout(drop_down_symbols, init_stock)

    # Callbacks for Home Page
    HomePageCallbacks.register_homepage_callbacks(app, init_stock)