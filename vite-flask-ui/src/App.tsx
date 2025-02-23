import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Provider } from "react-redux";
import { store } from "./store";
import StockSearch from "./components/StockSearch";
import StockDetails from "./components/StockDetails";

function App() {  
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          <Route path="/" element={<StockSearch />} />
          <Route path="/stock/:symbol" element={<StockDetails />} />
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;
