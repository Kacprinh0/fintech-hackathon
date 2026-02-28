import tkinter as tk
from tkinter import ttk, messagebox
import random

class SmartBasketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartBasket")
        self.root.geometry("950x600")
        self.root.configure(bg="#f4f6f9")

        self.basket = []

        self.create_title()
        self.create_input_section()
        self.create_basket_table()
        self.create_compare_button()
        self.create_results_section()

    # -----------------------------
    # UI SECTIONS
    # -----------------------------

    def create_title(self):
        title = tk.Label(
            self.root,
            text="🛒 SmartBasket",
            font=("Helvetica", 26, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50"
        )
        title.pack(pady=15)

    def create_input_section(self):
        frame = tk.Frame(self.root, bg="#f4f6f9")
        frame.pack(pady=10)

        tk.Label(frame, text="Item:", bg="#f4f6f9").grid(row=0, column=0, padx=5)
        self.item_entry = tk.Entry(frame, width=20)
        self.item_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Quantity:", bg="#f4f6f9").grid(row=0, column=2, padx=5)
        self.quantity_spin = tk.Spinbox(frame, from_=1, to=20, width=5)
        self.quantity_spin.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Size:", bg="#f4f6f9").grid(row=0, column=4, padx=5)
        self.size_entry = tk.Entry(frame, width=10)
        self.size_entry.grid(row=0, column=5, padx=5)

        add_btn = tk.Button(frame, text="Add Item", command=self.add_item, bg="#3498db", fg="white")
        add_btn.grid(row=0, column=6, padx=10)

    def create_basket_table(self):
        self.tree = ttk.Treeview(self.root, columns=("Item", "Qty", "Size"), show="headings")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Qty", text="Quantity")
        self.tree.heading("Size", text="Size")
        self.tree.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack()

        tk.Button(btn_frame, text="Remove Selected", command=self.remove_item, bg="#e74c3c", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Edit Selected", command=self.edit_item, bg="#f39c12", fg="white").pack(side="left", padx=5)

    def create_compare_button(self):
        tk.Button(
            self.root,
            text="Compare Supermarkets",
            command=self.compare_prices,
            bg="#2ecc71",
            fg="white",
            font=("Helvetica", 12, "bold")
        ).pack(pady=20)

    def create_results_section(self):
        self.results_tree = ttk.Treeview(self.root, columns=("Shop", "Total", "Savings"), show="headings")
        self.results_tree.heading("Shop", text="Shop Name")
        self.results_tree.heading("Total", text="Total Cost (£)")
        self.results_tree.heading("Savings", text="Savings vs Most Expensive (£)")
        self.results_tree.pack(pady=10)

        self.results_tree.tag_configure("cheapest", background="#d4edda")

    # -----------------------------
    # BASKET MANAGEMENT
    # -----------------------------

    def add_item(self):
        item = self.item_entry.get().strip()
        quantity = int(self.quantity_spin.get())
        size = self.size_entry.get().strip()

        if not item:
            messagebox.showwarning("Input Error", "Please enter an item name.")
            return

        self.basket.append((item, quantity, size))
        self.tree.insert("", "end", values=(item, quantity, size))

        self.item_entry.delete(0, tk.END)
        self.size_entry.delete(0, tk.END)

    def remove_item(self):
        selected = self.tree.selection()
        if not selected:
            return

        for item in selected:
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.basket[index]

    def edit_item(self):
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")

        self.item_entry.delete(0, tk.END)
        self.item_entry.insert(0, values[0])
        self.quantity_spin.delete(0, tk.END)
        self.quantity_spin.insert(0, values[1])
        self.size_entry.delete(0, tk.END)
        self.size_entry.insert(0, values[2])

        self.remove_item()

    # -----------------------------
    # PRICE SIMULATION ENGINE
    # -----------------------------

    def simulate_price(self, item):
        base_prices = {
            "milk": 1.50,
            "bread": 1.20,
            "eggs": 2.50,
            "chicken": 4.00,
            "rice": 1.80,
            "pasta": 1.10
        }

        base = base_prices.get(item.lower(), random.uniform(1.0, 5.0))
        return round(base + random.uniform(-0.4, 0.8), 2)

    def compare_prices(self):
        if not self.basket:
            messagebox.showwarning("Basket Empty", "Add items before comparing.")
            return

        supermarkets = ["Tesco", "Sainsbury's", "Aldi", "Asda", "Morrisons"]
        totals = {}

        for shop in supermarkets:
            total_cost = 0
            for item, qty, size in self.basket:
                price = self.simulate_price(item)
                total_cost += price * qty
            totals[shop] = round(total_cost, 2)

        self.display_results(totals)

    # -----------------------------
    # RESULTS DISPLAY
    # -----------------------------

    def display_results(self, totals):
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        cheapest = min(totals.values())
        most_expensive = max(totals.values())

        for shop, total in totals.items():
            savings = round(most_expensive - total, 2)
            tag = "cheapest" if total == cheapest else ""
            self.results_tree.insert("", "end", values=(shop, total, savings), tags=(tag,))


# -----------------------------
# RUN APPLICATION
# -----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBasketApp(root)
    root.mainloop()