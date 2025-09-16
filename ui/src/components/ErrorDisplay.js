import React from "react";
import { getErrorInfo, shouldRetry } from "../utils/errorHandler";

const ErrorDisplay = ({ error, onRetry, showDetails = false }) => {
  if (!error) return null;

  const errorInfo = getErrorInfo(error.type);
  const canRetry = shouldRetry(error.type);

  return (
    <div
      style={{
        padding: "20px",
        textAlign: "center",
        backgroundColor: "#f8f9fa",
        border: "1px solid #dee2e6",
        borderRadius: "8px",
        margin: "20px",
        maxWidth: "600px",
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      {/* Error Icon */}
      <div
        style={{
          fontSize: "48px",
          color: "#dc3545",
          marginBottom: "16px",
        }}
      >
        <span role="img" aria-label="Warning">
          ⚠️
        </span>
      </div>

      {/* Error Title */}
      <h2
        style={{
          color: "#dc3545",
          marginBottom: "12px",
          fontSize: "24px",
        }}
      >
        {errorInfo.title}
      </h2>

      {/* Error Message */}
      <p
        style={{
          color: "#6c757d",
          marginBottom: "16px",
          fontSize: "16px",
          lineHeight: "1.5",
        }}
      >
        {errorInfo.message}
      </p>

      {/* User Action */}
      <p
        style={{
          color: "#495057",
          marginBottom: "20px",
          fontSize: "14px",
          fontStyle: "italic",
        }}
      >
        {errorInfo.userAction}
      </p>

      {/* Retry Button */}
      {canRetry && onRetry && (
        <button
          onClick={onRetry}
          style={{
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            padding: "10px 20px",
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "16px",
            marginRight: "10px",
          }}
        >
          Retry
        </button>
      )}

      {/* Refresh Button */}
      <button
        onClick={() => window.location.reload()}
        style={{
          backgroundColor: "#6c757d",
          color: "white",
          border: "none",
          padding: "10px 20px",
          borderRadius: "4px",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        Refresh Page
      </button>

      {/* Technical Details (for debugging) */}
      {showDetails && (
        <details
          style={{
            marginTop: "20px",
            textAlign: "left",
            backgroundColor: "#f8f9fa",
            padding: "15px",
            borderRadius: "4px",
            border: "1px solid #dee2e6",
          }}
        >
          <summary
            style={{
              cursor: "pointer",
              fontWeight: "bold",
              marginBottom: "10px",
            }}
          >
            Technical Details
          </summary>
          <div style={{ fontSize: "12px", fontFamily: "monospace" }}>
            <p>
              <strong>Error Type:</strong> {error.type}
            </p>
            <p>
              <strong>Status Code:</strong> {error.statusCode || "N/A"}
            </p>
            <p>
              <strong>Message:</strong> {error.message}
            </p>
            {error.details && (
              <p>
                <strong>Details:</strong> {error.details}
              </p>
            )}
            <p>
              <strong>Timestamp:</strong> {error.timestamp}
            </p>
          </div>
        </details>
      )}
    </div>
  );
};

export default ErrorDisplay;
