import requests
from urllib.error import URLError, HTTPError
from app.exceptions import ServiceUnavailableException, DataProcessingException
from urllib.request import urlopen, Request

def safe_request_get(url, timeout=10, logger=None):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        error_msg = f"Timeout connecting to {url}"
        if logger:
            logger.error(error_msg)
        raise ServiceUnavailableException(error_msg)
    except requests.exceptions.ConnectionError:
        error_msg = f"Connection error with {url}"
        if logger:
            logger.error(error_msg)
        raise ServiceUnavailableException(error_msg)
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error {e.response.status_code} connecting to {url}"
        if logger:
            logger.error(error_msg)
        raise ServiceUnavailableException(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error connecting to {url}: {str(e)}"
        if logger:
            logger.error(error_msg)
        raise Exception(error_msg)


def safe_urlopen(url, headers=None, timeout=10, logger=None):
    
    try:
        if headers:
            request = Request(url, headers=headers)
        else:
            request = Request(url)
        
        response = urlopen(request, timeout=timeout)
        return response
    except URLError as e:
        error_msg = f"URL error connecting to {url}: {str(e)}"
        if logger:
            logger.error(error_msg)
        raise ServiceUnavailableException(error_msg)
    except HTTPError as e:
        error_msg = f"HTTP error {e.code} connecting to {url}"
        if logger:
            logger.error(error_msg)
        raise ServiceUnavailableException(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error connecting to {url}: {str(e)}"
        if logger:
            logger.error(error_msg)
        raise Exception(error_msg)


def safe_json_parse(response, logger=None):
    try:
        return response.json()
    except ValueError as e:
        error_msg = f"Error parsing JSON: {str(e)}"
        if logger:
            logger.error(error_msg)
        raise DataProcessingException("JSON parsing", error_msg)


