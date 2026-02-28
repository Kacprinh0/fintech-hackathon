import React, { useState } from 'react';

export default function ItemRow({ item, onChange, onRemove }) {
  const [name, setName] = useState(item.name);
  const [qty, setQty] = useState(item.quantity);

  const commit = () => {
    onChange({ name, quantity: qty });
  };

  return (
    <tr>
      <td>
        <input
          type="text"
          value={name}
          onBlur={commit}
          onChange={(e) => setName(e.target.value)}
        />
      </td>
      <td>
        <input
          type="number"
          min="1"
          value={qty}
          onBlur={commit}
          onChange={(e) => setQty(parseInt(e.target.value, 10))}
        />
      </td>
      <td>
        <button onClick={onRemove}>✕</button>
      </td>
    </tr>
  );
}
