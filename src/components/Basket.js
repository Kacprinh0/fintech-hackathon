import React, { useState } from 'react';
import ItemRow from './ItemRow';

export default function Basket({ items, setItems, compareBasket }) {
  const [name, setName] = useState('');
  const [qty, setQty] = useState(1);

  const addItem = () => {
    if (!name.trim()) return;
    setItems([...items, { name: name.trim(), quantity: qty }]);
    setName('');
    setQty(1);
  };

  const updateItem = (index, newItem) => {
    const copy = [...items];
    copy[index] = newItem;
    setItems(copy);
  };

  const removeItem = (index) => {
    const copy = items.filter((_, i) => i !== index);
    setItems(copy);
  };

  return (
    <section className="basket">
      <h2>Create your basket</h2>
      <div className="add-form">
        <input
          type="text"
          placeholder="Item name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="number"
          min="1"
          value={qty}
          onChange={(e) => setQty(parseInt(e.target.value, 10))}
        />
        <button onClick={addItem}>Add</button>
      </div>
      <table className="basket-table">
        <thead>
          <tr>
            <th>Item</th>
            <th>Qty</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {items.map((it, idx) => (
            <ItemRow
              key={idx}
              item={it}
              onChange={(ni) => updateItem(idx, ni)}
              onRemove={() => removeItem(idx)}
            />
          ))}
        </tbody>
      </table>
      <button className="compare-button" onClick={compareBasket}>
        Compare Basket
      </button>
    </section>
  );
}
