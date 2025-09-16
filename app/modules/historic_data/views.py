from flask import Response
import simplejson

from app.modules.cripto.views import get_binance_price, get_lemon_price
from app.modules.dollar_blue.views import get_dollar_price
from app.exceptions import ServiceUnavailableException, DataProcessingException
from .database import db


def write_historic_data(*args, **kwds):
    logger = kwds.get('logger')
    
    try:
        dolar_blue_prices = get_dollar_price(logger)
        dolar_blue = sum(dolar_blue_prices) / len(dolar_blue_prices)
        binance_price = get_binance_price(logger)
        lemon_price = get_lemon_price(logger)
        
        success = db.insert_data(
            dollar_blue_price=dolar_blue,
            lemon_price=lemon_price,
            binance_price=binance_price
        )
        
        if success:
            logger.info(f"Data inserted successfully: dollar_blue={dolar_blue}, lemon={lemon_price}, binance={binance_price}")
            output = {"success": True, "message": "Data saved successfully"}
            response = Response(simplejson.dumps(output), status=200, mimetype='application/json')
            return response
        else:
            logger.error("Failed to insert data into database")
            raise Exception("Failed to save data to database")
            
    except (ServiceUnavailableException, DataProcessingException):
        raise

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