import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import React, { useState, useEffect } from "react";

import ArrayStore from 'devextreme/data/array_store';
import List from 'devextreme-react/list';
import TileView from 'devextreme-react/tile-view';

import { data } from './data.js';
import axios from "axios";

import {
  Chart,
  Title,
  CommonSeriesSettings,
  Series,
  Legend,
  ArgumentAxis,
  ValueAxis
} from 'devextreme-react/chart';

export default function App() {

  const [selectedItem, setSelectedItem] = useState(data[0]);
  const [dolarBluePrice, setDolarBluePrice] = useState(0);
  const [criptoDolarPrice, setCriptoDolarPrice] = useState([]);
  const [historicalData, setHistoricalData] = useState([]);
  document.title = 'Dollar tool';

    const dataSourceOptions = {
      store: new ArrayStore({
        data,
        key: 'Id',
      }),
      group: 'Coin',
      searchExpr: ['Platform_Name', 'Coin'],
      sort: 'Price',
      // desc: false
    };

    const listAttrs = { class: 'list' };
    const tileViewAttrs = { class: 'tile' };
    const formatCurrency = new Intl.NumberFormat(
      'en-US', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      },
    ).format;


    const handleListSelectionChange = (e) => {
      setSelectedItem(e.addedItems[0])
    }
  
  
  function renderListGroup(group) {
    return <div className="coin">{group.key}</div>;
  }
  
  function renderListItem(item) {
    switch (item.Platform_Name) {
      case 'Dolar Blue':
        item.Price = (dolarBluePrice.dollar_blue_min+dolarBluePrice.dollar_blue_max)/2;
        break;
      case 'Binance P2P':
        item.Price = criptoDolarPrice.dollar_cripto_binance;
        break;
      case 'Lemon Cash':
        item.Price = criptoDolarPrice.dollar_cripto_lemon;
        break;
      default:
        item.Price = 0;
    }

    return (
      <div>
        <div className="platform">
          <div className="name">{item.Platform_Name}</div>
          <div className={`type ${item.Platform_Class.toLowerCase()}`} />
        </div>
        <div className="price-container">
          <div className="price">{formatCurrency(item.Price)}</div>
          &nbsp;
        </div>
      </div>
    );
  }
  
  function renderTile(item) {
    return (
      <div
        className="tile-image"
        style={{ backgroundImage: `url(${item.FileName})` }}
      />
    );
  }

  function returnMaxMinDolarBlue(item) {
    if (item.Platform_Name === "Dolar Blue")
    {
      return dolarBluePrice.dollar_blue_min + "/" + dolarBluePrice.dollar_blue_max
    }
  }


  useEffect(() => {
      {axios("../API/dollar_cripto")
        .then((response) => response.data)
        .then((data) => setCriptoDolarPrice(data));};
        {axios("../API/dollar_blue")
        .then((response) => response.data)
        .then((data) => setDolarBluePrice(data));}
        {axios("../API/get_historic_data")
        .then((response) => response.data)
        .then((data) => setHistoricalData(data));};
        setSelectedItem(data[0]);
  }, []);

  useEffect(() => {
    {axios("../API/dollar_cripto")
      .then((response) => response.data)
      .then((data) => setCriptoDolarPrice(data));};
      {axios("../API/dollar_blue")
      .then((response) => response.data)
      .then((data) => setDolarBluePrice(data));}
}, [selectedItem]);

const getChartValue = (item) =>
{
  let value = "";
  switch (item.Platform_Name) {
    case 'Dolar Blue':
      value = "dolarBlue";
      break;
    case 'Binance P2P':
      value = "dolarBinance"
      break;
    case 'Lemon Cash':
      value = "dolarLemon"
      break;
  }
    return value
}


  // ----------------------------------------------------------------
  


    return (
      <React.Fragment>
        <div className="left">
          <List
            selectionMode="single"
            dataSource={dataSourceOptions}
            grouped={true}
            searchEnabled={true}
            selectedItemKeys={selectedItem.Id}
            onSelectionChanged={handleListSelectionChange}
            itemRender={renderListItem}
            groupRender={renderListGroup}
            elementAttr={listAttrs}
            sort={selectedItem.Price}
          />
        </div>

        <div className="right">
          <div className="header">
            <div className="name-container">
              <div className="name">{selectedItem.Platform_Name}</div>
              <div className={`type ${selectedItem.Platform_Class.toLowerCase()}`} />
            </div>
            <div className="price-container">
              <div className="price">{formatCurrency(selectedItem.Price)}</div>
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

          <div className="buyandsell">{returnMaxMinDolarBlue(selectedItem)}</div>
          <div className="description">{selectedItem.Description}</div>

          <div className="down">
        <Chart
        id="chart"
        dataSource={historicalData}
      >
        <Title text={selectedItem.Platform_Name} subtitle="Rendimiento del último mes" />
        <CommonSeriesSettings argumentField="timestamp" type="line" />
        <Series valueField={getChartValue(selectedItem)} name="historicValues" />
        <Legend visible={false} />
        <ArgumentAxis argumentType="datetime" />
        <ValueAxis position="right" />
      </Chart>
      </div>

        </div>

      </React.Fragment>
    );
  }
