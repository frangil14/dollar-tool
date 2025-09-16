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
      style={{
        position: "fixed",
        bottom: "10px",
        right: "10px",
        padding: "10px 15px",
        borderRadius: "5px",
        fontSize: "12px",
        zIndex: 1000,
        display: "flex",
        alignItems: "center",
        gap: "10px",
        backgroundColor: "rgba(0, 0, 0, 0.4)",
        color: "#ffffff",
      }}
    >
      <div>
        <span style={{ opacity: 0.7 }}>Last update: </span>
        <span style={{ fontWeight: "bold" }}>
          {formatLastUpdated(lastUpdated)}
        </span>
      </div>

      <div style={{ display: "flex", gap: "5px" }}>
        <button
          onClick={onRefresh}
          disabled={loading}
          style={{
            background: "#007acc",
            color: "white",
            border: "none",
            padding: "5px 10px",
            borderRadius: "3px",
            cursor: loading ? "not-allowed" : "pointer",
            opacity: loading ? 0.5 : 1,
          }}
        >
          {loading ? (
            <span role="img" aria-label="Loading">
              ⏳
            </span>
          ) : (
            <span role="img" aria-label="Refresh">
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
            padding: "5px 10px",
            borderRadius: "3px",
            cursor: "pointer",
          }}
        >
          {isAutoRefreshActive ? (
            <span role="img" aria-label="Pause">
              ⏸️
            </span>
          ) : (
            <span role="img" aria-label="Play">
              ▶️
            </span>
          )}
        </button>
      </div>
    </div>
  );
};

export default StatusBar;
