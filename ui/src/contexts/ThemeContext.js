import React, { createContext, useContext, useState, useEffect } from "react";

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  // Initialize theme from localStorage or system preference
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
      return savedTheme === "dark";
    }
    // Check system preference
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });

  // Apply theme changes
  useEffect(() => {
    const theme = isDarkMode ? "dark" : "light";

    // Save to localStorage
    localStorage.setItem("theme", theme);

    // Apply to document
    document.documentElement.setAttribute("data-theme", theme);

    // Listen for system theme changes
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleSystemThemeChange = (e) => {
      // Only update if user hasn't manually set a preference
      if (!localStorage.getItem("theme")) {
        setIsDarkMode(e.matches);
      }
    };

    mediaQuery.addEventListener("change", handleSystemThemeChange);

    return () => {
      mediaQuery.removeEventListener("change", handleSystemThemeChange);
    };
  }, [isDarkMode]);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  const setTheme = (theme) => {
    setIsDarkMode(theme === "dark");
  };

  const value = {
    isDarkMode,
    theme: isDarkMode ? "dark" : "light",
    toggleTheme,
    setTheme,
  };

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
};
