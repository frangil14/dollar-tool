from .views import get_dollar_blue


def add_routes_module(app, logger):
    app.add_url_rule('/API/dollar_blue', view_func=get_dollar_blue, defaults={'logger': logger})
    return app
