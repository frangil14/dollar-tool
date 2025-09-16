from flask import Response
import simplejson
from app.config import Config
from app.exceptions import ServiceUnavailableException, DataProcessingException
from app.utils.general_utils import safe_request_get, safe_json_parse


def get_dollar_cripto(*args, **kwds):
    logger = kwds.get('logger')
    
    try:
        lemon_price = get_lemon_price(logger)
        binance_price = get_binance_price(logger)

        output = {"dollar_cripto_lemon": lemon_price, "dollar_cripto_binance": binance_price}
        response = Response(simplejson.dumps(output, ignore_nan=True),
                            status=200, mimetype='application/json')
        return response
    except (ServiceUnavailableException, DataProcessingException):
        raise

def get_lemon_price(logger=None):
    try:
        response = safe_request_get(Config.CRIPTOYA_URL, logger=logger)
        data = safe_json_parse(response, logger)
        
        if "lemoncash" not in data:
            raise DataProcessingException("LemonCash", "Field 'lemoncash' not found in response")
        
        lemon = data["lemoncash"]
        if "totalBid" not in lemon:
            raise DataProcessingException("LemonCash", "Field 'totalBid' not found in LemonCash data")
        
        return float(lemon["totalBid"])
    except (ServiceUnavailableException, DataProcessingException):
        raise

def get_binance_price(logger=None):
    try:
        response = safe_request_get(Config.CRIPTOYA_URL, logger=logger)
        data = safe_json_parse(response, logger)
        
        if "binancep2p" not in data:
            raise DataProcessingException("Binance P2P", "Field 'binancep2p' not found in response")
        
        binance = data["binancep2p"]
        if "totalBid" not in binance:
            raise DataProcessingException("Binance P2P", "Field 'totalBid' not found in Binance P2P data")
        
        return float(binance["totalBid"])
    except (ServiceUnavailableException, DataProcessingException):
        raise
