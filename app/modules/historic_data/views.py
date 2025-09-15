from datetime import datetime
from flask import Response
import simplejson

from app.modules.cripto.views import get_binance_price, get_lemon_price
from app.modules.dollar_blue.views import get_dollar_price
from .database import db

# TESTING
# http://localhost:5000/API/write_historic_data
# http://localhost:5000/API/get_historic_data


def write_historic_data(*args, **kwds):
    """
    Escribir datos históricos a la base de datos SQLite.
    Obtiene precios actuales y los almacena con timestamp.
    """
    logger = kwds.get('logger')
    
    try:
        # Obtener precios actuales
        dolar_blue_prices = get_dollar_price()
        dolar_blue = sum(dolar_blue_prices) / len(dolar_blue_prices)
        binance_price = get_binance_price()
        lemon_price = get_lemon_price()
        
        # Insertar en la base de datos
        success = db.insert_data(
            dollar_blue_price=dolar_blue,
            lemon_price=lemon_price,
            binance_price=binance_price
        )
        
        if success:
            logger.info(f"Data inserted successfully: dollar_blue={dolar_blue}, lemon={lemon_price}, binance={binance_price}")
            output = {"success": True, "message": "Data saved successfully"}
            status = 200
        else:
            logger.error("Failed to insert data into database")
            output = {"success": False, "error": "Failed to save data"}
            status = 500
            
    except Exception as e:
        logger.error(f"Error in write_historic_data: {e}")
        output = {"success": False, "error": str(e)}
        status = 500
    
    response = Response(simplejson.dumps(output), status=status, mimetype='application/json')
    return response

def get_historic_data(*args, **kwds):
    """
    Obtener datos históricos de la base de datos SQLite.
    Retorna el mismo formato que el Excel anterior.
    """
    logger = kwds.get('logger')
    
    try:
        # Obtener datos de la base de datos
        data = db.get_historic_data()
        
        if data:
            # Convertir timestamps a strings para JSON (igual que Excel)
            for record in data:
                if record.get('timestamp'):
                    # Si ya es string, dejarlo como está; si es datetime, convertirlo
                    if hasattr(record['timestamp'], 'isoformat'):
                        record['timestamp'] = record['timestamp'].isoformat()
            
            logger.info(f"Retrieved {len(data)} historic records")
            # Mismo formato que Excel: array directo de registros
            output = data
            status = 200
        else:
            logger.info("No historic data found")
            output = []
            status = 200
            
    except Exception as e:
        logger.error(f"Error in get_historic_data: {e}")
        output = {"error": str(e)}
        status = 500
    
    response = Response(simplejson.dumps(output, ignore_nan=True), status=status, mimetype='application/json')
    return response