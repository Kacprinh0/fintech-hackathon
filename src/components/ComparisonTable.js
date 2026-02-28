import React, { useState } from 'react';

export default function ComparisonTable({ results }) {
  const [expanded, setExpanded] = useState(null);
  const { shopResults, cheapest, mostExp } = results;

  const toggle = (idx) => {
    setExpanded(expanded === idx ? null : idx);
  };

  return (
    <section className="comparison">
      <h2>Comparison Results</h2>
      <table className="results-table">
        <thead>
          <tr>
            <th>Shop</th>
            <th>Total</th>
            <th>Savings</th>
          </tr>
        </thead>
        <tbody>
          {shopResults.map((r, idx) => {
            const savings = (mostExp - r.total).toFixed(2);
            const cheapestClass = r.total === cheapest ? 'cheapest' : '';
            const expensiveClass = r.total === mostExp ? 'expensive' : '';
            return (
              <React.Fragment key={idx}>
                <tr
                  className={`${cheapestClass} ${expensiveClass}`}
                  onClick={() => toggle(idx)}
                >
                  <td>{r.shop}</td>
                  <td>£{r.total.toFixed(2)}</td>
                  <td>£{savings}</td>
                </tr>
                {expanded === idx && (
                  <tr className="breakdown-row">
                    <td colSpan="3">
                      <ul>
                        {r.breakdown.map((b, bi) => (
                          <li key={bi}>
                            {b.item} — £{b.price.toFixed(2)}{' '}
                            {!b.found && '(not found)'}
                          </li>
                        ))}
                      </ul>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            );
          })}
        </tbody>
      </table>
    </section>
  );
}
