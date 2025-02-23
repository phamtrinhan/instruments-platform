import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';

const BASE_URL = 'http://localhost:5173/api/v1/stocks';

export interface Instrument {
  id: number;
  name: string;
  symbol: string;
  price: number;
}

interface InstrumentState {
  items: Instrument[];
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

const initialState: InstrumentState = {
  items: [],
  status: 'idle',
  error: null,
};

// Async thunks
export const fetchInstruments = createAsyncThunk<Instrument[]>(
  'instruments/fetchInstruments',
  async () => {
    const response = await axios.get(BASE_URL);
    return response.data;
  }
);

export const addInstrument = createAsyncThunk<Instrument, Omit<Instrument, 'id'>>(
  'instruments/addInstrument',
  async (newInstrument) => {
    const response = await axios.post(BASE_URL, newInstrument);
    return response.data;
  }
);

export const deleteInstrument = createAsyncThunk<number, number>(
  'instruments/deleteInstrument',
  async (id) => {
    await axios.delete(`${BASE_URL}/${id}`);
    return id;
  }
);

const instrumentSlice = createSlice({
  name: 'instruments',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInstruments.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchInstruments.fulfilled, (state, action: PayloadAction<Instrument[]>) => {
        state.status = 'succeeded';
        state.items = action.payload;
      })
      .addCase(fetchInstruments.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message || 'Failed to fetch instruments';
      })
      .addCase(addInstrument.fulfilled, (state, action: PayloadAction<Instrument>) => {
        state.items.push(action.payload);
      })
      .addCase(deleteInstrument.fulfilled, (state, action: PayloadAction<number>) => {
        state.items = state.items.filter((instrument) => instrument.id !== action.payload);
      });
  },
});

export default instrumentSlice.reducer;
