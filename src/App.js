import React, { useState, useEffect } from 'react';
import Basket from './components/Basket';
import ComparisonTable from './components/ComparisonTable';
import priceData from './data/prices.json';

function App() {
  const [basket, setBasket] = useState(() => {
    const saved = localStorage.getItem('smartbasket');
    return saved ? JSON.parse(saved) : [];
  });
  const [results, setResults] = useState(null);
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('smartbasket-dark');
    return saved === 'true';
  });

  useEffect(() => {
    localStorage.setItem('smartbasket', JSON.stringify(basket));
  }, [basket]);

  useEffect(() => {
    localStorage.setItem('smartbasket-dark', darkMode);
  }, [darkMode]);

  const compareBasket = () => {
    const normalize = (s) => s.trim().toLowerCase();
    const match = (item, products) => {
      const name = normalize(item.name);
      // naive match: find product whose name includes all words
      let best = null;
      let bestScore = 0;
      products.forEach((p) => {
        const pn = normalize(p.name);
        let score = 0;
        name.split(' ').forEach((w) => {
          if (pn.includes(w)) score += 1;
        });
        if (score > bestScore) {
          bestScore = score;
          best = p;
        }
      });
      return best;
    };

    const shopResults = priceData.shops.map((shop) => {
      let total = 0;
      const breakdown = [];
      basket.forEach((item) => {
        const product = match(item, shop.products);
        const price = product ? product.price * item.quantity : 0;
        total += price;
        breakdown.push({
          item: item.name,
          price: product ? product.price : 0,
          found: !!product,
        });
      });
      return { shop: shop.name, total, breakdown };
    });

    const cheapest = Math.min(...shopResults.map((r) => r.total));
    const mostExp = Math.max(...shopResults.map((r) => r.total));
    setResults({ shopResults, cheapest, mostExp });
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      <header className="header">
        <h1>SmartBasket</h1>
        <button onClick={() => setDarkMode((d) => !d)}>
          {darkMode ? 'Light Mode' : 'Dark Mode'}
        </button>
      </header>
      <main>
        <Basket items={basket} setItems={setBasket} compareBasket={compareBasket} />
        {results && <ComparisonTable results={results} />}
      </main>
    </div>
  );
}

export default App;
