from flask import Response
import simplejson
from .config import CRIPTOYA_URL, CRIPTOYA_URL_BINANCE
import requests

# TESTING
# http://localhost:5000/API/dollar_cripto


def get_dollar_cripto(*args, **kwds):
    logger = kwds.get('logger')
    response = requests.get(CRIPTOYA_URL)
    data = response.json()
    lemon = data["lemoncash"]
    lemon_price = float(lemon["totalBid"])

    response = requests.get(CRIPTOYA_URL_BINANCE)
    data = response.json()
    data = data["data"]
    numeric_data = [float(x["adv"]["price"]) for x in data]
    average_price = sum(numeric_data) / len(numeric_data)

    # -------------- Return JSON ------------------
    output = {"dollar_cripto_lemon": lemon_price, "dollar_cripto_binance": average_price}
    response = Response(simplejson.dumps(output, ignore_nan=True),
                        status=200, mimetype='application/json')
    return response
