import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { fetchInstruments } from "../features/stocks/stockSlice"; // Import the Redux thunk
import { RootState, AppDispatch } from "../store"; // Redux store types

const StockSearch: React.FC = () => {
  const [query, setQuery] = useState<string>(""); // User input for search query
  const [filteredStocks, setFilteredStocks] = useState<any[]>([]); // Filtered stock list
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();

  // Redux state
  const stocks = useSelector((state: RootState) => state.stocks.items);
  const status = useSelector((state: RootState) => state.stocks.status);
  const error = useSelector((state: RootState) => state.stocks.error);

  // Fetch stocks from Redux store on component mount
  useEffect(() => {
    if (status === "idle") {
      dispatch(fetchInstruments());
    }
  }, [status, dispatch]);

  // Update filtered stocks when stocks or query changes
  useEffect(() => {
    if (query) {
      const filtered = stocks.filter(
        (stock) =>
          stock.name.toLowerCase().includes(query.toLowerCase()) ||
          stock.symbol.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredStocks(filtered);
    } else {
      setFilteredStocks(stocks);
    }
  }, [query, stocks]);

  // Navigate to stock details page
  const handleStockClick = (symbol: string) => {
    navigate(`/stock/${symbol}`);
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center", color: "teal" }}>Stock Search</h1>

      <input
        type="text"
        placeholder="Enter stock name or symbol..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{
          width: "100%",
          padding: "0.5rem",
          fontSize: "1rem",
          borderRadius: "5px",
          border: "1px solid #ccc",
          marginBottom: "1rem",
        }}
      />

      {status === "loading" && <p style={{ textAlign: "center" }}>Loading stocks...</p>}
      {status === "failed" && (
        <p style={{ textAlign: "center", color: "red" }}>Error: {error}</p>
      )}

      {query && (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {filteredStocks.length > 0 ? (
            filteredStocks.map((stock) => (
              <li
                key={stock.symbol}
                onClick={() => handleStockClick(stock.symbol)}
                style={{
                  padding: "0.5rem",
                  margin: "0.5rem 0",
                  border: "1px solid #ddd",
                  borderRadius: "5px",
                  backgroundColor: "#f9f9f9",
                  cursor: "pointer",
                }}
              >
                <strong>
                  {stock.name} ({stock.symbol})
                </strong>
                <br />
                Price: ${stock.price.toFixed(2)}
              </li>
            ))
          ) : (
            <li style={{ textAlign: "center", color: "gray" }}>No stocks found.</li>
          )}
        </ul>
      )}
    </div>
  );
};

export default StockSearch;
