from .views import write_historic_data, get_historic_data

def add_routes_module(app, logger):
    app.add_url_rule('/API/write_historic_data', view_func=write_historic_data, defaults={'logger': logger})
    app.add_url_rule('/API/get_historic_data', view_func=get_historic_data, defaults={'logger': logger})
    return app
