from flask import Response
import simplejson
from app.config import Config
import re
from bs4 import BeautifulSoup
from app.exceptions import ServiceUnavailableException, DataProcessingException
from app.utils.general_utils import safe_urlopen

COUNT_DATA_SOURCES = 2


def get_dollar_blue(*args, **kwds,):
    logger = kwds.get('logger')
    
    try:
        dollar_price = get_dollar_price(logger)

        output = {"dollar_blue_min": min(dollar_price),"dollar_blue_max": max(dollar_price)}
        response = Response(simplejson.dumps(output, ignore_nan=True),
                            status=200, mimetype='application/json')
        return response
    except (ServiceUnavailableException, DataProcessingException):
        raise


def get_price_dolarhoy(logger=None):
    try:
        page = safe_urlopen(Config.DOLARHOY_URL, logger=logger)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        
        target_divs = soup.find_all('div', class_='tile cotizacion_value')
        
        if not target_divs:
            raise DataProcessingException("DolarHoy", "No elements found with class 'tile cotizacion_value'")
        
        numbers = re.findall(r'\$(\d+,\d+)', target_divs[0].get_text())
        
        if not numbers:
            raise DataProcessingException("DolarHoy", "No prices found in expected format")
        
        prices = []
        for num in numbers:
            try:
                price = float(num.replace(",", "."))
                prices.append(price)
            except ValueError:
                if logger:
                    logger.warning(f"DolarHoy: Error converting price '{num}' to float")
                continue
        
        if not prices:
            raise DataProcessingException("DolarHoy", "Could not process prices")
        
        return prices
    except (ServiceUnavailableException, DataProcessingException):
        raise


def get_price_cronista(logger=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        page = safe_urlopen(Config.CRONISTA_URL, headers=headers, logger=logger)
        html_bytes = page.read()
        html = html_bytes.decode("ISO-8859-1")
        soup = BeautifulSoup(html, 'html.parser')
        
        target_sections = soup.find_all('section', class_='piece markets standard boxed')
        
        if not target_sections:
            raise DataProcessingException("Cronista", "No sections found with class 'piece markets standard boxed'")
        
        section = target_sections[0]
        prices = []
        
        sell_span = section.find('span', class_='sell')
        if sell_span:
            sell_text = sell_span.get_text()
            sell_match = re.search(r'\$(\d+\.\d+,\d+)', sell_text)
            if sell_match:
                try:
                    sell_price = float(sell_match.group(1).replace(".", "").replace(",", "."))
                    prices.append(sell_price)
                except ValueError:
                    if logger:
                        logger.warning(f"Cronista: Error converting sell price '{sell_match.group(1)}' to float")
        
        buy_span = section.find('span', class_='buy')
        if buy_span:
            buy_text = buy_span.get_text()
            buy_match = re.search(r'\$(\d+\.\d+,\d+)', buy_text)
            if buy_match:
                try:
                    buy_price = float(buy_match.group(1).replace(".", "").replace(",", "."))
                    prices.append(buy_price)
                except ValueError:
                    if logger:
                        logger.warning(f"Cronista: Error converting buy price '{buy_match.group(1)}' to float")

        if not prices:
            raise DataProcessingException("Cronista", "Could not extract valid prices")
        
        return prices
    except (ServiceUnavailableException, DataProcessingException):
        raise

def get_dollar_price(logger=None):
    try:
        dolarhoy_price = get_price_dolarhoy(logger)
        cronista_price = get_price_cronista(logger)

        if not dolarhoy_price or not cronista_price:
            raise DataProcessingException("Quotation service", "Could not get prices from all sources")

        minimum = (min(dolarhoy_price) + min(cronista_price))/COUNT_DATA_SOURCES
        maximum = (max(dolarhoy_price) + max(cronista_price))/COUNT_DATA_SOURCES

        return [minimum, maximum]
    except (ServiceUnavailableException, DataProcessingException):
        raise