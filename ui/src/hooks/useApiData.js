import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { parseApiError } from "../utils/errorHandler";

const useApiData = (refreshInterval = 30000) => {
  // 30 seconds by default
  const [dolarBluePrice, setDolarBluePrice] = useState({});
  const [criptoDolarPrice, setCriptoDolarPrice] = useState({});
  const [historicalData, setHistoricalData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [errors, setErrors] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const intervalRef = useRef(null);

  const fetchData = async (isInitialLoad = false) => {
    try {
      if (isInitialLoad) {
        setLoading(true);
      }
      setError(null);
      setErrors([]);

      // Make all calls in parallel with individual error handling
      const results = await Promise.allSettled([
        axios.get("../API/dollar_blue"),
        axios.get("../API/dollar_cripto"),
        axios.get("../API/get_historic_data"),
      ]);

      const [dollarBlueResult, criptoResult, historicResult] = results;
      const newErrors = [];

      // Process results - only update if endpoint was successful
      if (dollarBlueResult.status === "fulfilled") {
        setDolarBluePrice(dollarBlueResult.value.data);
      } else {
        const error = parseApiError(dollarBlueResult.reason);
        newErrors.push({ ...error, endpoint: "dollar_blue" });
        console.error("Dollar Blue Error:", error);
        // Don't update state if it fails - keep previous data
      }

      if (criptoResult.status === "fulfilled") {
        setCriptoDolarPrice(criptoResult.value.data);
      } else {
        const error = parseApiError(criptoResult.reason);
        newErrors.push({ ...error, endpoint: "dollar_cripto" });
        console.error("Crypto Error:", error);
        // Don't update state if it fails - keep previous data
      }

      if (historicResult.status === "fulfilled") {
        setHistoricalData(historicResult.value.data);
      } else {
        const error = parseApiError(historicResult.reason);
        newErrors.push({ ...error, endpoint: "historic_data" });
        console.error("Historic Data Error:", error);
        // Don't update state if it fails - keep previous data
      }

      // If all failed, show general error
      if (newErrors.length === 3) {
        setError(newErrors[0]);
      } else {
        setErrors(newErrors);
      }

      setLastUpdated(new Date());
    } catch (err) {
      console.error("Unexpected error:", err);
      const parsedError = parseApiError(err);
      setError(parsedError);
    } finally {
      if (isInitialLoad) {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    // Initial load
    fetchData(true);

    // Setup auto-refresh
    intervalRef.current = setInterval(() => {
      fetchData(false);
    }, refreshInterval);

    // Cleanup on unmount
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [refreshInterval]);

  const refetch = () => {
    fetchData(false);
  };

  const stopAutoRefresh = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const startAutoRefresh = () => {
    if (!intervalRef.current) {
      intervalRef.current = setInterval(() => {
        fetchData(false);
      }, refreshInterval);
    }
  };

  return {
    dolarBluePrice,
    criptoDolarPrice,
    historicalData,
    loading,
    error,
    errors,
    lastUpdated,
    refetch,
    stopAutoRefresh,
    startAutoRefresh,
  };
};

export default useApiData;
