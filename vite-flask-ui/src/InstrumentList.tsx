import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchInstruments, addInstrument, deleteInstrument } from './features/stocks/stockSlice'; // Updated import path
import { RootState, AppDispatch } from './store';

// Define the type for the new instrument form
interface NewInstrument {
  name: string;
  type: string;
  price: string;
}

const InstrumentList: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();

  // Access state from Redux
  const instruments = useSelector((state: RootState) => state.stocks.items); // Use 'stocks' as the slice name
  const status = useSelector((state: RootState) => state.stocks.status);
  const error = useSelector((state: RootState) => state.stocks.error);

  // Local state for the new instrument form
  const [newInstrument, setNewInstrument] = useState<NewInstrument>({
    name: '',
    type: '',
    price: '',
  });

  // Fetch instruments when the component mounts or if the status changes
  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchInstruments());
    }
  }, [status, dispatch]);

  // Handle adding a new instrument
  const handleAddInstrument = () => {
    if (!newInstrument.name || !newInstrument.type || !newInstrument.price) {
      alert('All fields are required!');
      return;
    }

    dispatch(
      addInstrument({
        name: newInstrument.name,
        symbol: newInstrument.type,
        price: parseFloat(newInstrument.price),
      })
    );

    // Reset the form
    setNewInstrument({ name: '', type: '', price: '' });
  };

  // Handle deleting an instrument
  const handleDeleteInstrument = (id: number) => {
    dispatch(deleteInstrument(id));
  };

  return (
    <div>
      <h1>Instruments</h1>
      {status === 'loading' && <p>Loading instruments...</p>}
      {status === 'failed' && <p>Error: {error}</p>}

      <ul>
        {instruments.map((instrument) => (
          <li key={instrument.id}>
            {instrument.name} - {instrument.symbol} - ${instrument.price}
            <button onClick={() => handleDeleteInstrument(instrument.id)}>Delete</button>
          </li>
        ))}
      </ul>

      <h2>Add New Instrument</h2>
      <input
        type="text"
        placeholder="Name"
        value={newInstrument.name}
        onChange={(e) => setNewInstrument({ ...newInstrument, name: e.target.value })}
      />
      <input
        type="text"
        placeholder="Type"
        value={newInstrument.type}
        onChange={(e) => setNewInstrument({ ...newInstrument, type: e.target.value })}
      />
      <input
        type="number"
        placeholder="Price"
        value={newInstrument.price}
        onChange={(e) => setNewInstrument({ ...newInstrument, price: e.target.value })}
      />
      <button onClick={handleAddInstrument}>Add</button>
    </div>
  );
};

export default InstrumentList;
