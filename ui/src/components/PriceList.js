import React from "react";
import ArrayStore from "devextreme/data/array_store";
import List from "devextreme-react/list";

const PriceList = ({
  data,
  selectedItem,
  onSelectionChange,
  dolarBluePrice,
  criptoDolarPrice,
}) => {
  const dataSourceOptions = {
    store: new ArrayStore({
      data,
      key: "Id",
    }),
    group: "Coin",
    searchExpr: ["Platform_Name", "Coin"],
    sort: "Price",
  };

  const listAttrs = { class: "list" };

  const formatCurrency = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format;

  const getPriceForPlatform = (platformName) => {
    switch (platformName) {
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

  const renderListGroup = (group) => {
    return <div className="coin">{group.key}</div>;
  };

  const renderListItem = (item) => {
    const price = getPriceForPlatform(item.Platform_Name);

    return (
      <div>
        <div className="platform">
          <div className="name">{item.Platform_Name}</div>
          <div className={`type ${item.Platform_Class.toLowerCase()}`} />
        </div>
        <div className="price-container">
          <div className="price">{price ? formatCurrency(price) : "N/A"}</div>
          &nbsp;
        </div>
      </div>
    );
  };

  return (
    <div className="left">
      <List
        selectionMode="single"
        dataSource={dataSourceOptions}
        grouped={true}
        searchEnabled={true}
        selectedItemKeys={selectedItem.Id}
        onSelectionChanged={onSelectionChange}
        itemRender={renderListItem}
        groupRender={renderListGroup}
        elementAttr={listAttrs}
        sort={selectedItem.Price}
      />
    </div>
  );
};

export default PriceList;
