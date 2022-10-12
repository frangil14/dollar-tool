from datetime import datetime, timedelta
from flask import Response
import os
import simplejson

from app.utils.mongo_connector import MongoConnector
from .models import CleanParquetFiles

# TESTING
# http://localhost:5000/API/get_parquets_to_clean
# http://localhost:5000/API/get_parquets_in_server

def get_parquets_to_clean(*args, **kwds):
    logger = kwds.get('logger')

    output = []
    mongo_connector = MongoConnector()
    mongo_connector.set_db("test")

    clean = CleanParquetFiles(logger, mongo_connector)


    data = clean.get_parquets_to_clean()
    for record in data:
        output.append(record)


    response = Response(simplejson.dumps(output, ignore_nan=True, default=str), status=200,
                        mimetype='application/json')
    return response

def get_last_used_parquets(*args, **kwds):
    logger = kwds.get('logger')

    output = []
    mongo_connector = MongoConnector()
    mongo_connector.set_db("test")

    clean = CleanParquetFiles(logger, mongo_connector)


    data = clean.get_last_used_parquets()
    for record in data:
        output.append(record)


    response = Response(simplejson.dumps(output, ignore_nan=True, default=str), status=200,
                        mimetype='application/json')
    return response


def get_parquets_in_server(*args, **kwds):

    logger = kwds.get('logger')

    clean = CleanParquetFiles(logger)
    output = clean.get_parquets_in_server()

    response = Response(simplejson.dumps(output, ignore_nan=True, default=str), status=200,
                        mimetype='application/json')
    return response

def clean_parquets(*args, **kwds):
    logger = kwds.get('logger')

    clean = CleanParquetFiles(logger)

    limit_date = datetime.today() - timedelta(days=5)
    removed = []

    data = clean.get_parquets_in_server()
    for file, lastAccessTime_str in data:
        lastAccessTime = datetime.strptime(lastAccessTime_str, "%Y-%m-%d %H:%M:%S")
        if lastAccessTime < limit_date:
            if os.path.isfile(file):
                os.remove(file)
                removed.append(file)

    if len(removed)>0:
        logger.info(f'The following files were removed: {removed}')

    response = Response(simplejson.dumps(removed, ignore_nan=True, default=str), status=200,
                        mimetype='application/json')
    return response