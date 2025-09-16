import React from "react";
import TileView from "devextreme-react/tile-view";

const PriceCard = ({ selectedItem, dolarBluePrice, criptoDolarPrice }) => {
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
        if (dolarBluePrice.dollar_blue_min && dolarBluePrice.dollar_blue_max) {
          return (
            (dolarBluePrice.dollar_blue_min + dolarBluePrice.dollar_blue_max) /
            2
          );
        }
        return null;
      case "Binance P2P":
        return criptoDolarPrice.dollar_cripto_binance || null;
      case "Lemon Cash":
        return criptoDolarPrice.dollar_cripto_lemon || null;
      default:
        return null;
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
    if (
      selectedItem.Platform_Name === "Blue Dollar" &&
      dolarBluePrice.dollar_blue_min &&
      dolarBluePrice.dollar_blue_max
    ) {
      const min = formatCurrency(dolarBluePrice.dollar_blue_min);
      const max = formatCurrency(dolarBluePrice.dollar_blue_max);
      return `Buy: ${min} | Sell: ${max}`;
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
            {getPriceForSelectedItem()
              ? formatCurrency(getPriceForSelectedItem())
              : "N/A"}
            {selectedItem.Platform_Name === "Blue Dollar" &&
              getPriceForSelectedItem() && (
                <span
                  style={{ fontSize: "12px", opacity: 0.7, marginLeft: "8px" }}
                >
                  (average)
                </span>
              )}
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
