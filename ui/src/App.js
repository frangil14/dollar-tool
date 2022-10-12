import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import React, { useState, useEffect } from "react";

import ArrayStore from 'devextreme/data/array_store';
import List from 'devextreme-react/list';
import TileView from 'devextreme-react/tile-view';

import { data } from './data.js';
import axios from "axios";

export default function App() {

    const dataSourceOptions = {
      store: new ArrayStore({
        data,
        key: 'Id',
      }),
      group: 'Coin',
      searchExpr: ['Platform_Name', 'Coin'],
      sort: 'Price',
      desc: false
    };

    const listAttrs = { class: 'list' };
    const tileViewAttrs = { class: 'tile' };
    const formatCurrency = new Intl.NumberFormat(
      'en-US', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
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
        item.Price = dolarBluePrice.dollar_blue_average_price;
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
        style={{ backgroundImage: `url(images/hotels/${item.FileName})` }}
      />
    );
  }


  const [selectedItem, setSelectedItem] = useState(data[0]);
  const [dolarBluePrice, setDolarBluePrice] = useState(0);
  const [criptoDolarPrice, setCriptoDolarPrice] = useState([]);

  useEffect(() => {
      {axios("../API/dollar_cripto")
        .then((response) => response.data)
        .then((data) => setCriptoDolarPrice(data));};
        {axios("../API/dollar_blue")
        .then((response) => response.data)
        .then((data) => setDolarBluePrice(data));}
  }, []);

  useEffect(() => {
    {axios("../API/dollar_cripto")
      .then((response) => response.data)
      .then((data) => setCriptoDolarPrice(data));};
      {axios("../API/dollar_blue")
      .then((response) => response.data)
      .then((data) => setDolarBluePrice(data));}
}, selectedItem);

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

          <div className="address">{selectedItem.Postal_Code}, {selectedItem.Address}</div>
          <div className="description">{selectedItem.Description}</div>
        </div>
      </React.Fragment>
    );
  }
