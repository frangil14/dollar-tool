import logging
import traceback
from datetime import datetime
from flask import Response
import simplejson

from .exceptions import APIException


def create_error_response(message: str, status_code: int, error_code: str = "API_ERROR", details: str = None) -> Response:
    error_data = {
        "error": True,
        "message": message,
        "error_code": error_code,
        "timestamp": datetime.now().isoformat() + "Z"
    }
    
    if details:
        error_data["details"] = details
    
    return Response(
        simplejson.dumps(error_data, ignore_nan=True),
        status=status_code,
        mimetype='application/json'
    )


def register_error_handlers(app, logger: logging.Logger = None):
    @app.errorhandler(APIException)
    def handle_api_exception(error: APIException):
        if logger:
            logger.error(f"API Exception: {error.error_code} - {error.message}")
        
        return create_error_response(
            message=error.message,
            status_code=error.status_code,
            error_code=error.error_code,
            details=getattr(error, 'details', None)
        )
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error: Exception):
        if logger:
            logger.error(f"Unhandled Exception: {type(error).__name__}: {str(error)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
        
        return create_error_response(
            message="Internal server error",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            details=str(error)
        )
