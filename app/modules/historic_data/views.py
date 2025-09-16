from flask import Response
import simplejson

from app.modules.cripto.views import get_binance_price, get_lemon_price
from app.modules.dollar_blue.views import get_dollar_price
from app.exceptions import ServiceUnavailableException, DataProcessingException
from .database import db


def write_historic_data(*args, **kwds):
    logger = kwds.get('logger')
    
    dollar_blue_price = None
    lemon_price = None
    binance_price = None
    errors = []
    
    try:
        dolar_blue_prices = get_dollar_price(logger)
        dollar_blue_price = sum(dolar_blue_prices) / len(dolar_blue_prices)
        logger.info(f"Dollar blue price obtained: {dollar_blue_price}")
    except (ServiceUnavailableException, DataProcessingException) as e:
        errors.append(f"Dollar blue: {e.message}")
        logger.warning(f"Could not get dollar blue price: {e.message}")
    except Exception as e:
        errors.append(f"Dollar blue: {str(e)}")
        logger.warning(f"Unexpected error getting dollar blue price: {str(e)}")
    
    try:
        lemon_price = get_lemon_price(logger)
        logger.info(f"Lemon price obtained: {lemon_price}")
    except (ServiceUnavailableException, DataProcessingException) as e:
        errors.append(f"Lemon: {e.message}")
        logger.warning(f"Could not get lemon price: {e.message}")
    except Exception as e:
        errors.append(f"Lemon: {str(e)}")
        logger.warning(f"Unexpected error getting lemon price: {str(e)}")
    
    try:
        binance_price = get_binance_price(logger)
        logger.info(f"Binance price obtained: {binance_price}")
    except (ServiceUnavailableException, DataProcessingException) as e:
        errors.append(f"Binance: {e.message}")
        logger.warning(f"Could not get binance price: {e.message}")
    except Exception as e:
        errors.append(f"Binance: {str(e)}")
        logger.warning(f"Unexpected error getting binance price: {str(e)}")
    
    # If no price was obtained from any source, raise an error
    if dollar_blue_price is None and lemon_price is None and binance_price is None:
        error_message = "Could not obtain any price data from external sources"
        logger.error(f"{error_message}. Errors: {', '.join(errors)}")
        raise ServiceUnavailableException("All price sources", error_message)
    
    # Try to insert the data into the database
    try:
        success = db.insert_data(
            dollar_blue_price=dollar_blue_price,
            lemon_price=lemon_price,
            binance_price=binance_price
        )
        
        if success:
            obtained_prices = []
            if dollar_blue_price is not None:
                obtained_prices.append(f"dollar_blue={dollar_blue_price}")
            if lemon_price is not None:
                obtained_prices.append(f"lemon={lemon_price}")
            if binance_price is not None:
                obtained_prices.append(f"binance={binance_price}")
            
            logger.info(f"Data inserted successfully: {', '.join(obtained_prices)}")
            
            output = {
                "success": True, 
                "message": "Data saved successfully",
                "saved_data": {
                    "dollar_blue": dollar_blue_price,
                    "lemon": lemon_price,
                    "binance": binance_price
                }
            }
            
            if errors:
                output["partial_errors"] = errors
                output["message"] = f"Data saved successfully (some sources unavailable: {len(errors)})"
            
            response = Response(simplejson.dumps(output), status=200, mimetype='application/json')
            return response
        else:
            logger.error("Failed to insert data into database")
            raise Exception("Failed to save data to database")
            
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise Exception(f"Failed to save data to database: {str(e)}")

def get_historic_data(*args, **kwds):
    logger = kwds.get('logger')
    
    try:
        data = db.get_historic_data()
        
        if data:
            for record in data:
                if record.get('timestamp'):
                    if hasattr(record['timestamp'], 'isoformat'):
                        record['timestamp'] = record['timestamp'].isoformat()
            
            logger.info(f"Retrieved {len(data)} historic records")
            output = data
        else:
            logger.info("No historic data found")
            output = []
            
        response = Response(simplejson.dumps(output, ignore_nan=True), status=200, mimetype='application/json')
        return response
            
    except Exception as e:
        logger.error(f"Error in get_historic_data: {e}")
        raise Exception(f"Error retrieving historic data: {str(e)}")