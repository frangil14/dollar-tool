class APIException(Exception):
    def __init__(self, message: str, status_code: int = 500, error_code: str = "API_ERROR", details: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class ServiceUnavailableException(APIException):
    def __init__(self, error_msg: str = "Service temporarily unavailable", details: str = None):
        super().__init__(
            message=f"{error_msg}",
            status_code=503,
            error_code="SERVICE_UNAVAILABLE",
            details=details
        )


class DataProcessingException(APIException):
    def __init__(self, error_msg: str = "Data processing error", details: str = None):
        super().__init__(
            message=f"{error_msg}",
            status_code=422,
            error_code="DATA_PROCESSING_ERROR",
            details=details
        )
