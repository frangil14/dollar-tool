from flask import Response
import simplejson
from .config import CRIPTOYA_URL
import requests


def get_dollar_cripto(*args, **kwds):
    logger = kwds.get('logger')
    lemon_price = get_lemon_price()
    binance_price = get_binance_price()

    # -------------- Return JSON ------------------
    output = {"dollar_cripto_lemon": lemon_price, "dollar_cripto_binance": binance_price}
    response = Response(simplejson.dumps(output, ignore_nan=True),
                        status=200, mimetype='application/json')
    return response

def get_lemon_price():
    response = requests.get(CRIPTOYA_URL)
    data = response.json()
    lemon = data["lemoncash"]
    return float(lemon["totalBid"])

def get_binance_price():
    response = requests.get(CRIPTOYA_URL)
    data = response.json()
    binance = data["binancep2p"]
    return float(binance["totalBid"])
