import React from "react";

const StatusBar = ({
  lastUpdated,
  loading,
  onRefresh,
  onStopAutoRefresh,
  onStartAutoRefresh,
  isAutoRefreshActive = true,
}) => {
  const formatLastUpdated = (date) => {
    if (!date) return "Never";

    const now = new Date();
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);

    if (seconds < 60) {
      return `${seconds} seconds ago`;
    } else if (minutes < 60) {
      return `${minutes} minutes ago`;
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
        background: "rgba(0, 0, 0, 0.8)",
        color: "white",
        padding: "10px 15px",
        borderRadius: "5px",
        fontSize: "12px",
        zIndex: 1000,
        display: "flex",
        alignItems: "center",
        gap: "10px",
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
          {loading ? "⏳" : "🔄"}
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
          {isAutoRefreshActive ? "⏸️" : "▶️"}
        </button>
      </div>
    </div>
  );
};

export default StatusBar;
