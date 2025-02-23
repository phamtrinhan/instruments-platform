import { configureStore } from "@reduxjs/toolkit";
import stockReducer from "./features/stocks/stockSlice";

export const store = configureStore({
  reducer: {
    stocks: stockReducer,
  },
});

// Infer types for RootState and AppDispatch
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
