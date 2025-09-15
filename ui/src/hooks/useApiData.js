import { useState, useEffect, useRef } from "react";
import axios from "axios";

const useApiData = (refreshInterval = 30000) => {
  // 30 segundos por defecto
  const [dolarBluePrice, setDolarBluePrice] = useState({});
  const [criptoDolarPrice, setCriptoDolarPrice] = useState({});
  const [historicalData, setHistoricalData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const intervalRef = useRef(null);

  const fetchData = async (isInitialLoad = false) => {
    try {
      if (isInitialLoad) {
        setLoading(true);
      }
      setError(null);

      // Hacer todas las llamadas en paralelo
      const [
        dollarBlueResponse,
        criptoResponse,
        historicResponse,
      ] = await Promise.all([
        axios.get("../API/dollar_blue"),
        axios.get("../API/dollar_cripto"),
        axios.get("../API/get_historic_data"),
      ]);

      setDolarBluePrice(dollarBlueResponse.data);
      setCriptoDolarPrice(criptoResponse.data);
      setHistoricalData(historicResponse.data);
      setLastUpdated(new Date());
    } catch (err) {
      console.error("Error fetching data:", err);
      setError(err.message || "Error al cargar los datos");
    } finally {
      if (isInitialLoad) {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    // Carga inicial
    fetchData(true);

    // Configurar auto-refresh
    intervalRef.current = setInterval(() => {
      fetchData(false);
    }, refreshInterval);

    // Cleanup al desmontar
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
    lastUpdated,
    refetch,
    stopAutoRefresh,
    startAutoRefresh,
  };
};

export default useApiData;
