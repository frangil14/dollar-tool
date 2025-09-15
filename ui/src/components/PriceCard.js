import React from "react";
import TileView from "devextreme-react/tile-view";

const PriceCard = ({ selectedItem, dolarBluePrice }) => {
  const tileViewAttrs = { class: "tile" };

  const formatCurrency = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format;

  const getPriceForSelectedItem = () => {
    switch (selectedItem.Platform_Name) {
      case "Blue Dollar":
        return (
          (dolarBluePrice.dollar_blue_min + dolarBluePrice.dollar_blue_max) / 2
        );
      case "Binance P2P":
        return dolarBluePrice.dollar_blue_min; // Placeholder - will be updated with real data
      case "Lemon Cash":
        return dolarBluePrice.dollar_blue_min; // Placeholder - will be updated with real data
      default:
        return 0;
    }
  };

  const renderTile = (item) => {
    return (
      <div
        className="tile-image"
        style={{ backgroundImage: `url(${item.FileName})` }}
      />
    );
  };

  const getMaxMinDolarBlue = () => {
    if (selectedItem.Platform_Name === "Blue Dollar") {
      return `${dolarBluePrice.dollar_blue_min}/${dolarBluePrice.dollar_blue_max}`;
    }
    return null;
  };

  return (
    <div className="right">
      <div className="header">
        <div className="name-container">
          <div className="name">{selectedItem.Platform_Name}</div>
          <div
            className={`type ${selectedItem.Platform_Class.toLowerCase()}`}
          />
        </div>
        <div className="price-container">
          <div className="price">
            {formatCurrency(getPriceForSelectedItem())}
          </div>
        </div>
      </div>

      <TileView
        dataSource={selectedItem.Images}
        height={224}
        baseItemHeight={100}
        baseItemWidth={137}
        itemMargin={12}
        noDataText=""
        itemRender={renderTile}
        elementAttr={tileViewAttrs}
      />

      <div className="buyandsell">{getMaxMinDolarBlue()}</div>
      <div className="description">{selectedItem.Description}</div>
    </div>
  );
};

export default PriceCard;
