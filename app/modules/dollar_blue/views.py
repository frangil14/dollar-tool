from flask import Response
import simplejson
from urllib.request import urlopen, Request
from .config import DOLARHOY_URL, CRONISTA_URL
import re
from bs4 import BeautifulSoup

# Constants
NUM_FUENTES_DATOS = 2


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
    soup = BeautifulSoup(html, 'html.parser')
    
    # ===== SELECTOR PARA DOLARHOY =====
    target_divs = soup.find_all('div', class_='tile cotizacion_value')
    
    if target_divs:
        numbers = re.findall(r'\$(\d+,\d+)', target_divs[0].get_text())
        
        if numbers:
            prices = []
            for num in numbers:
                price = float(num.replace(",", "."))
                prices.append(price)
            return prices
    
    return []


def get_price_cronista(*args, **kwds,):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    page = Request(CRONISTA_URL, headers=headers)
    response = urlopen(page)
    html_bytes = response.read()
    html = html_bytes.decode("ISO-8859-1")
    soup = BeautifulSoup(html, 'html.parser')
    
    # ===== SELECTOR PARA CRONISTA =====
    target_sections = soup.find_all('section', class_='piece markets standard boxed')
    
    if target_sections:
        section = target_sections[0]
        
        # Valor de venta
        sell_span = section.find('span', class_='sell')
        if sell_span:
            sell_text = sell_span.get_text()
            sell_match = re.search(r'\$(\d+\.\d+,\d+)', sell_text)
            if sell_match:
                sell_price = float(sell_match.group(1).replace(".", "").replace(",", "."))
            else:
                sell_price = None
        else:
            sell_price = None
        
        # Valor de compra
        buy_span = section.find('span', class_='buy')
        if buy_span:
            buy_text = buy_span.get_text()
            buy_match = re.search(r'\$(\d+\.\d+,\d+)', buy_text)
            if buy_match:
                buy_price = float(buy_match.group(1).replace(".", "").replace(",", "."))
            else:
                buy_price = None
        else:
            buy_price = None
        
        prices = []
        if buy_price:
            prices.append(buy_price)
        if sell_price:
            prices.append(sell_price)

        return prices
    else:
        return []

def get_dollar_price():
    dolarhoy_price = get_price_dolarhoy()
    cronista_price = get_price_cronista()

    minimum = (min(dolarhoy_price) + min(cronista_price))/NUM_FUENTES_DATOS
    maximum = (max(dolarhoy_price) + max(cronista_price))/NUM_FUENTES_DATOS

    return [minimum, maximum]