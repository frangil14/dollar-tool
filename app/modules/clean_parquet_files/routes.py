from .views import get_parquets_to_clean, get_last_used_parquets, get_parquets_in_server, clean_parquets

def add_routes_module(app, logger):
    app.add_url_rule('/API/get_parquets_to_clean', view_func=get_parquets_to_clean, defaults={'logger': logger})
    app.add_url_rule('/API/get_last_used_parquets', view_func=get_last_used_parquets, defaults={'logger': logger})
    app.add_url_rule('/API/get_parquets_in_server', view_func=get_parquets_in_server, defaults={'logger': logger})
    app.add_url_rule('/API/clean_parquets', view_func=clean_parquets, defaults={'logger': logger})
    return app
