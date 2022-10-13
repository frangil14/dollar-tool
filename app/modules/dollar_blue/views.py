from flask import Response
import simplejson
from urllib.request import urlopen
from .config import DOLARHOY_URL, KEY_WORDS, UNION
import re

# TESTING
# http://localhost:5000/API/dollar_blue


def get_dollar_blue(*args, **kwds,):
    logger = kwds.get('logger')
    page = urlopen(DOLARHOY_URL)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    
    pattern = UNION.join(KEY_WORDS)

    match_results = re.search(pattern, html, re.IGNORECASE)

    data = match_results.group()
    data = re.sub("<.*?>", "", data) # Remove HTML tags

    data = re.findall(r'\d+\.\d+', data)
    numeric_data = get_dollar_price()

    # -------------- Return JSON ------------------
    output = {"dollar_blue_min": min(numeric_data),"dollar_blue_max": max(numeric_data)}
    response = Response(simplejson.dumps(output, ignore_nan=True),
                        status=200, mimetype='application/json')
    return response

def get_dollar_price():
    page = urlopen(DOLARHOY_URL)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    
    pattern = UNION.join(KEY_WORDS)

    match_results = re.search(pattern, html, re.IGNORECASE)

    data = match_results.group()
    data = re.sub("<.*?>", "", data) # Remove HTML tags

    data = re.findall(r'\d+\.\d+', data)
    return [float(x) for x in data]