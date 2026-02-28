# SmartBasket

A modern responsive React application that lets users compare grocery basket prices across multiple supermarkets and identify the cheapest option.

## Features

- Create and manage a basket of items (name, quantity, size)
- Compare prices across mock supermarkets (Tesco, Sainsbury's, Aldi, etc.)
- View total cost per shop with savings and detailed breakdowns
- Highlights cheapest and most expensive shops
- Dark/light mode toggle
- Basket saved to local storage
- Responsive layout for mobile and desktop

## Getting Started

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Run the development server**
   ```bash
   npm start
   ```

3. Open http://localhost:3000 in your browser.

4. Add items to your basket and click **Compare Basket** to see shop pricing comparisons.

## Project Structure

- `src/` – React source code
  - `components/` – Reusable UI components
  - `data/` – Mock pricing JSON
  - `styles.css` – Global styles including dark mode
- `public/` – Static HTML

## Notes

This is a prototype with a simple matching algorithm. You can extend by integrating real APIs, adding dietary filters, brand toggles, or saving past baskets.