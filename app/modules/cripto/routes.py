from .views import get_dollar_cripto


def add_routes_module(app, logger):
    app.add_url_rule('/API/dollar_cripto', view_func=get_dollar_cripto, defaults={'logger': logger})
    return app
