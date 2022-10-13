from datetime import datetime
from flask import Response
import os
import pandas as pd
import simplejson

from app.modules.cripto.views import get_binance_price, get_lemon_price
from app.modules.dollar_blue.views import get_dollar_price
from app.utils.general_utils import parseTimestampToString
from .config import FILENAME, LOCAL_PATH, COLUMN_NAMES

# TESTING
# http://localhost:5000/API/write_historic_data
# http://localhost:5000/API/get_historic_data


def write_historic_data(*args, **kwds):
    logger = kwds.get('logger')

    path = os.path.join(os.getcwd(),LOCAL_PATH,FILENAME)

    if (not os.path.exists(path)):
        # We create the file because it does not exists
        print(path)
        df = pd.DataFrame(columns = COLUMN_NAMES)
        df.to_excel(path)
        logger.info(f'{path} file was successfully created.')

    # Read the excel file

    df = pd.read_excel(path, index_col=0)  

    dolar_blue_prices = get_dollar_price()
    dolar_blue = sum(dolar_blue_prices) / len(dolar_blue_prices)
    binance_price = get_binance_price()
    lemon_price = get_lemon_price()
    now = datetime.now()

    df.loc[len(df.index)] = [now, dolar_blue, lemon_price, binance_price]

    writer = pd.ExcelWriter(path, engine = 'openpyxl', mode='a',if_sheet_exists='replace')
    df.to_excel(writer)

    writer.save()
    writer.close()

    output = {"success": True}
    response = Response(output, status=200,
                        mimetype='application/json')
    return response

def get_historic_data(*args, **kwds):
    logger = kwds.get('logger')

    path = os.path.join(os.getcwd(),LOCAL_PATH,FILENAME)

    if (os.path.exists(path)):
        # Read the excel file
        df = pd.read_excel(path, index_col=0)  
        data_frame_parsed = df.apply(parseTimestampToString)
        output = data_frame_parsed.to_dict(orient='records')
        response = Response(simplejson.dumps(output, ignore_nan=True), status=200,
                            mimetype='application/json')
    else:
        output = {"error":"historic data file not found"}
        response = Response(output, status=404,
                            mimetype='application/json')

    return response