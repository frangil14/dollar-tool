// Error handling utilities for API responses

export const ERROR_TYPES = {
  SERVICE_UNAVAILABLE: "SERVICE_UNAVAILABLE",
  DATA_PROCESSING_ERROR: "DATA_PROCESSING_ERROR",
  INTERNAL_SERVER_ERROR: "INTERNAL_SERVER_ERROR",
  NETWORK_ERROR: "NETWORK_ERROR",
  UNKNOWN_ERROR: "UNKNOWN_ERROR",
};

export const ERROR_MESSAGES = {
  [ERROR_TYPES.SERVICE_UNAVAILABLE]: {
    title: "Service Temporarily Unavailable",
    message:
      "External data sources are currently unavailable. Please try again later.",
    userAction: "Retry in a few minutes",
  },
  [ERROR_TYPES.DATA_PROCESSING_ERROR]: {
    title: "Data Processing Error",
    message: "There was an issue processing the data from external sources.",
    userAction: "Try refreshing the page",
  },
  [ERROR_TYPES.INTERNAL_SERVER_ERROR]: {
    title: "Internal Server Error",
    message: "An unexpected error occurred on our servers.",
    userAction: "Please contact support if this persists",
  },
  [ERROR_TYPES.NETWORK_ERROR]: {
    title: "Network Error",
    message:
      "Unable to connect to the server. Please check your internet connection.",
    userAction: "Check your connection and try again",
  },
  [ERROR_TYPES.UNKNOWN_ERROR]: {
    title: "Unknown Error",
    message: "An unexpected error occurred.",
    userAction: "Please try again or contact support",
  },
};

export const parseApiError = (error) => {
  // Network errors (no response)
  if (!error.response) {
    return {
      type: ERROR_TYPES.NETWORK_ERROR,
      statusCode: null,
      message: error.message || "Network error",
      details: null,
      timestamp: new Date().toISOString(),
    };
  }

  // API errors with response
  const { status, data } = error.response;

  // Check if it's our structured error format
  if (data && data.error && data.error_code) {
    return {
      type: data.error_code,
      statusCode: status,
      message: data.message,
      details: data.details,
      timestamp: data.timestamp,
    };
  }

  // Fallback for non-structured errors
  return {
    type: ERROR_TYPES.UNKNOWN_ERROR,
    statusCode: status,
    message: (data && data.message) || `HTTP ${status} Error`,
    details: (data && data.details) || null,
    timestamp: new Date().toISOString(),
  };
};

export const getErrorInfo = (errorType) => {
  return ERROR_MESSAGES[errorType] || ERROR_MESSAGES[ERROR_TYPES.UNKNOWN_ERROR];
};

export const shouldRetry = (errorType) => {
  const retryableErrors = [
    ERROR_TYPES.SERVICE_UNAVAILABLE,
    ERROR_TYPES.NETWORK_ERROR,
  ];
  return retryableErrors.includes(errorType);
};
