import React, { useState } from "react";

const StatusBanner = ({ errors, onRetry }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!errors || errors.length === 0) return null;

  const hasRetryableErrors = errors.some(
    (error) =>
      error.type === "SERVICE_UNAVAILABLE" || error.type === "NETWORK_ERROR"
  );

  const getBannerStyle = () => {
    const hasCriticalErrors = errors.some(
      (error) => error.type === "INTERNAL_SERVER_ERROR"
    );

    if (hasCriticalErrors) {
      return {
        backgroundColor: "#f8d7da",
        border: "1px solid #f5c6cb",
        color: "#721c24",
      };
    }

    return {
      backgroundColor: "#fff3cd",
      border: "1px solid #ffeaa7",
      color: "#856404",
    };
  };

  const bannerStyle = getBannerStyle();

  return (
    <div
      style={{
        ...bannerStyle,
        borderRadius: "4px",
        padding: "12px",
        margin: "10px",
        position: "relative",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center" }}>
          <span style={{ fontSize: "20px", marginRight: "8px" }}>
            {errors.length === 1 ? (
              <span role="img" aria-label="Warning">
                ⚠️
              </span>
            ) : (
              <span role="img" aria-label="Tools">
                🔧
              </span>
            )}
          </span>
          <span style={{ fontWeight: "bold" }}>
            {errors.length === 1
              ? "One data source is unavailable"
              : `${errors.length} data sources are unavailable`}
          </span>
        </div>

        <div>
          {hasRetryableErrors && onRetry && (
            <button
              onClick={onRetry}
              style={{
                backgroundColor: bannerStyle.color,
                color: "white",
                border: "none",
                padding: "6px 12px",
                borderRadius: "4px",
                cursor: "pointer",
                fontSize: "14px",
                marginRight: "8px",
              }}
            >
              Retry
            </button>
          )}

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            style={{
              backgroundColor: "transparent",
              border: "none",
              cursor: "pointer",
              fontSize: "14px",
              color: bannerStyle.color,
            }}
          >
            {isExpanded ? "Hide Details" : "Show Details"}
          </button>
        </div>
      </div>

      {isExpanded && (
        <div
          style={{
            marginTop: "12px",
            paddingTop: "12px",
            borderTop: `1px solid ${bannerStyle.border}`,
          }}
        >
          {errors.map((error, index) => (
            <div
              key={index}
              style={{
                marginBottom: "8px",
                padding: "8px",
                backgroundColor: "rgba(255,255,255,0.5)",
                borderRadius: "4px",
                fontSize: "14px",
              }}
            >
              <div style={{ fontWeight: "bold" }}>
                {error.type.replace(/_/g, " ")}
              </div>
              <div style={{ marginTop: "4px" }}>{error.message}</div>
              {error.details && (
                <div
                  style={{
                    fontSize: "12px",
                    marginTop: "4px",
                    fontFamily: "monospace",
                    opacity: 0.8,
                  }}
                >
                  {error.details}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default StatusBanner;
