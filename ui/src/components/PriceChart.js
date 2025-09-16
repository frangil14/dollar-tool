import React from "react";
import {
  Chart,
  Title,
  CommonSeriesSettings,
  Series,
  Legend,
  ArgumentAxis,
  ValueAxis,
} from "devextreme-react/chart";
import { useTheme } from "../contexts/ThemeContext";

const PriceChart = ({ selectedItem, historicalData }) => {
  const { isDarkMode } = useTheme();
  const getChartValue = (platformName) => {
    switch (platformName) {
      case "Blue Dollar":
        return "dolarBlue";
      case "Binance P2P":
        return "dolarBinance";
      case "Lemon Cash":
        return "dolarLemon";
      default:
        return "dolarBlue";
    }
  };

  return (
    <div className="down">
      <Chart id="chart" dataSource={historicalData}>
        <Title
          text={selectedItem.Platform_Name}
          subtitle={{
            text: "Historical Performance",
            font: {
              color: isDarkMode ? "#b3b3b3" : "#6c757d",
            },
          }}
          font={{
            color: isDarkMode ? "#ffffff" : "#212529",
          }}
        />
        <CommonSeriesSettings argumentField="timestamp" type="line" />
        <Series
          valueField={getChartValue(selectedItem.Platform_Name)}
          name="historicValues"
        />
        <Legend visible={false} />
        <ArgumentAxis argumentType="datetime" />
        <ValueAxis position="right" />
      </Chart>
    </div>
  );
};

export default PriceChart;
