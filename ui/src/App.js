import "devextreme/dist/css/dx.common.css";
import "devextreme/dist/css/dx.light.css";
import React, { useState } from "react";

import { data } from "./data.js";
import useApiData from "./hooks/useApiData";
import PriceList from "./components/PriceList";
import PriceCard from "./components/PriceCard";
import PriceChart from "./components/PriceChart";
import StatusBar from "./components/StatusBar";

export default function App() {
  const [selectedItem, setSelectedItem] = useState(data[0]);
  const [isAutoRefreshActive, setIsAutoRefreshActive] = useState(true);

  const {
    dolarBluePrice,
    criptoDolarPrice,
    historicalData,
    loading,
    error,
    lastUpdated,
    refetch,
    stopAutoRefresh,
    startAutoRefresh,
  } = useApiData(30000); // 30 segundos

  document.title = "Dollar tool";

  const handleListSelectionChange = (e) => {
    setSelectedItem(e.addedItems[0]);
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleToggleAutoRefresh = () => {
    if (isAutoRefreshActive) {
      stopAutoRefresh();
      setIsAutoRefreshActive(false);
    } else {
      startAutoRefresh();
      setIsAutoRefreshActive(true);
    }
  };

  // Show loading or error if necessary
  if (loading) {
    return (
      <div style={{ padding: "20px", textAlign: "center" }}>
        <h2>Loading data...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "20px", textAlign: "center", color: "red" }}>
        <h2>Error: {error}</h2>
        <p>Could not load data. Please refresh the page.</p>
      </div>
    );
  }

  return (
    <React.Fragment>
      <PriceList
        data={data}
        selectedItem={selectedItem}
        onSelectionChange={handleListSelectionChange}
        dolarBluePrice={dolarBluePrice}
        criptoDolarPrice={criptoDolarPrice}
      />

      <PriceCard selectedItem={selectedItem} dolarBluePrice={dolarBluePrice} />

      <PriceChart selectedItem={selectedItem} historicalData={historicalData} />

      <StatusBar
        lastUpdated={lastUpdated}
        loading={loading}
        onRefresh={handleRefresh}
        onStopAutoRefresh={handleToggleAutoRefresh}
        onStartAutoRefresh={handleToggleAutoRefresh}
        isAutoRefreshActive={isAutoRefreshActive}
      />
    </React.Fragment>
  );
}
