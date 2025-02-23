import React from "react";
import { useParams } from "react-router-dom";
import { stockData } from "./mockStocks";
import BuySellPage from "./BuySellPage";

const StockDetails: React.FC = () => {
  const { symbol } = useParams<{ symbol: string }>();
  const stock = stockData.find((item) => item.symbol === symbol);

  if (!stock) {
    return <div>Stock not found!</div>;
  }

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto" }}>
      <h1>{stock.name} ({stock.symbol})</h1>
      <p><strong>Price:</strong> ${stock.price.toFixed(2)}</p>
      <p><strong>Market Cap:</strong> {stock.marketCap}</p>
      <p><strong>Daily Change:</strong> {stock.dailyChange}</p>
      <p><strong>Description:</strong> {stock.description}</p>
      <BuySellPage stockSymbol={stock.symbol} stockPrice={stock.price} />
    </div>
  );
};

export default StockDetails;
