import React from "react";
import { useTheme } from "../contexts/ThemeContext";

const ThemeToggle = () => {
  const { isDarkMode, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      style={{
        position: "fixed",
        top: "20px",
        right: "20px",
        zIndex: 1000,
        background: "rgba(0, 123, 255, 0.7)",
        color: "#ffffff",
        border: "none",
        borderRadius: "50%",
        width: "45px",
        height: "45px",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "18px",
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)",
        transition: "all 0.3s ease",
        backdropFilter: "blur(4px)",
      }}
      onMouseEnter={(e) => {
        e.target.style.transform = "scale(1.1)";
      }}
      onMouseLeave={(e) => {
        e.target.style.transform = "scale(1)";
      }}
      title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
      aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
    >
      {isDarkMode ? "☀️" : "🌙"}
    </button>
  );
};

export default ThemeToggle;
