import React, { useState, useEffect } from "react";

const StatusBar = ({
  lastUpdated,
  loading,
  onRefresh,
  onStopAutoRefresh,
  onStartAutoRefresh,
  isAutoRefreshActive = true,
}) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  // Update current time every second for live counter
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const formatLastUpdated = (date) => {
    if (!date) return "Never";

    const diff = currentTime - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (seconds < 60) {
      return `${seconds} seconds ago`;
    } else if (minutes < 60) {
      return `${minutes} minutes ago`;
    } else if (hours < 24) {
      return `${hours} hours ago`;
    } else {
      return date.toLocaleTimeString();
    }
  };

  return (
    <div
      className="statusbar"
      style={{
        position: "fixed",
        bottom: "20px",
        right: "20px",
        padding: "4px 8px",
        borderRadius: "6px",
        fontSize: "11px",
        zIndex: 1000,
        display: "flex",
        alignItems: "center",
        gap: "8px",
        backgroundColor: "rgba(0, 0, 0, 0.6)",
        color: "#ffffff",
        backdropFilter: "blur(3px)",
        boxShadow: "0 1px 4px rgba(0, 0, 0, 0.1)",
      }}
    >
      <div>
        <span style={{ opacity: 0.7 }}>Last update: </span>
        <span style={{ fontWeight: "bold" }}>
          {formatLastUpdated(lastUpdated)}
        </span>
      </div>

      <div style={{ display: "flex", gap: "4px" }}>
        <button
          onClick={onRefresh}
          disabled={loading}
          style={{
            background: "#007acc",
            color: "white",
            border: "none",
            padding: "3px 6px",
            borderRadius: "3px",
            cursor: loading ? "not-allowed" : "pointer",
            opacity: loading ? 0.5 : 1,
            fontSize: "10px",
          }}
        >
          {loading ? (
            <span role="img" aria-label="Loading" style={{ fontSize: "15px" }}>
              ⏳
            </span>
          ) : (
            <span role="img" aria-label="Refresh" style={{ fontSize: "15px" }}>
              🔄
            </span>
          )}
        </button>

        <button
          onClick={isAutoRefreshActive ? onStopAutoRefresh : onStartAutoRefresh}
          style={{
            background: isAutoRefreshActive ? "#dc3545" : "#28a745",
            color: "white",
            border: "none",
            padding: "3px 6px",
            borderRadius: "3px",
            cursor: "pointer",
            fontSize: "10px",
          }}
        >
          {isAutoRefreshActive ? (
            <span role="img" aria-label="Pause" style={{ fontSize: "15px" }}>
              ⏸️
            </span>
          ) : (
            <span role="img" aria-label="Play" style={{ fontSize: "15px" }}>
              ▶️
            </span>
          )}
        </button>
      </div>
    </div>
  );
};

export default StatusBar;
