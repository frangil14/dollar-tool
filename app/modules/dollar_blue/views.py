from flask import Response
import simplejson
from urllib.request import urlopen, Request
from .config import DOLARHOY_URL, UNION, CRONISTA_URL, KEY_WORDS
import re

# TESTING
# http://localhost:5000/API/dollar_blue


def get_dollar_blue(*args, **kwds,):
    logger = kwds.get('logger')
    dollar_price = get_dollar_price()

    # -------------- Return JSON ------------------
    output = {"dollar_blue_min": min(dollar_price),"dollar_blue_max": max(dollar_price)}
    response = Response(simplejson.dumps(output, ignore_nan=True),
                        status=200, mimetype='application/json')
    return response


def get_price_dolarhoy():
    page = urlopen(DOLARHOY_URL)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    
    pattern = UNION.join(KEY_WORDS["dolarhoy"])

    match_results = re.search(pattern, html, re.IGNORECASE)

    data = match_results.group()
    data = re.sub("<.*?>", "", data) # Remove HTML tags

    data = re.findall(r'\d+\.\d+', data)
    return [float(x) for x in data]


def get_price_cronista(*args, **kwds,):
    page = Request(CRONISTA_URL, headers={"User-Agent": "Mozilla/5.0"})
    html_bytes = urlopen(page).read()
    html = html_bytes.decode("ISO-8859-1")
    
    pattern = UNION.join(KEY_WORDS["cronista"])
    match_results = re.search(pattern, html, re.IGNORECASE)

    data = match_results.group()
    data = re.sub("<.*?>", "", data) # Remove HTML tags

    data = re.findall(r'\d+\,\d', data)

    numeric_data = [float(x.replace(",", ".")) for x in data]

    filtered = filter(lambda score: score >= (sum(numeric_data) / len(numeric_data)/2), numeric_data)

    return list(filtered)

def get_dollar_price():
    dolarhoy_price = get_price_dolarhoy()
    cronista_price = get_price_cronista()

    #print(dolarhoy_price)
    #print(cronista_price)

    minimum = (min(dolarhoy_price) + min(cronista_price))/len(KEY_WORDS)
    maximum = (max(dolarhoy_price) + max(cronista_price))/len(KEY_WORDS)

    return [minimum, maximum]