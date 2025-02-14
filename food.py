import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Excel File Names
menu_file = "food_menu.xlsx"
order_file = "order_history.xlsx"

# Load Food Menu from Excel
try:
    df = pd.read_excel(menu_file, engine="openpyxl")
    menus = {}
    for _, row in df.iterrows():
        shop, item, price, category = row["Shop Name"], row["Food Item"], row["Price (₹)"], row["Category"]
        if shop not in menus:
            menus[shop] = {}
        menus[shop][item] = (price, category)
except FileNotFoundError:
    messagebox.showerror("Error", f"File '{menu_file}' not found.")
    exit()

class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery System")
        self.root.geometry("550x600")
        self.root.configure(bg="#222831")

        # Header Label
        tk.Label(root, text="Online Food Delivery", font=("Arial", 18, "bold"), fg="#EEEEEE", bg="#222831").pack(pady=10)

        # Customer Name
        tk.Label(root, text="Customer Name:", font=("Arial", 12), fg="#EEEEEE", bg="#222831").pack()
        self.customer_entry = tk.Entry(root, font=("Arial", 12), width=30)
        self.customer_entry.pack(pady=5)

        # Shop Selection
        tk.Label(root, text="Select a Shop:", font=("Arial", 12), fg="#EEEEEE", bg="#222831").pack()
        self.shop_var = tk.StringVar(value=list(menus.keys())[0])
        self.shop_menu = ttk.Combobox(root, textvariable=self.shop_var, values=list(menus.keys()), state="readonly", font=("Arial", 12))
        self.shop_menu.pack(pady=5)
        self.shop_menu.bind("<<ComboboxSelected>>", self.update_menu)

        # Menu Listbox with Scrollbar
        frame = tk.Frame(root, bg="#222831")
        frame.pack()
        self.menu_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, font=("Arial", 12), height=10, width=40, bg="#393E46", fg="white")
        self.scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.menu_listbox.yview)
        self.menu_listbox.config(yscrollcommand=self.scrollbar.set)
        self.menu_listbox.pack(side="left")
        self.scrollbar.pack(side="right", fill="y")
        self.update_menu(None)

        # Buttons
        self.order_button = tk.Button(root, text="Place Order", font=("Arial", 12, "bold"), bg="#00ADB5", fg="white", command=self.place_order)
        self.order_button.pack(pady=5, ipadx=10, ipady=5)

        self.bill_button = tk.Button(root, text="Generate Bill", font=("Arial", 12, "bold"), bg="#00ADB5", fg="white", command=self.generate_bill)
        self.bill_button.pack(pady=5, ipadx=10, ipady=5)

        self.revenue_button = tk.Button(root, text="View Revenue", font=("Arial", 12, "bold"), bg="#00ADB5", fg="white", command=self.display_revenue)
        self.revenue_button.pack(pady=5, ipadx=10, ipady=5)

        self.customers_button = tk.Button(root, text="View Customers", font=("Arial", 12, "bold"), bg="#00ADB5", fg="white", command=self.display_customers)
        self.customers_button.pack(pady=5, ipadx=10, ipady=5)

        # Order Summary Label
        self.order_summary = tk.Label(root, text="", font=("Arial", 12, "italic"), fg="lime", bg="#222831")
        self.order_summary.pack(pady=10)

    def update_menu(self, event):
        """Update menu list when shop is selected"""
        self.menu_listbox.delete(0, tk.END)
        shop_name = self.shop_var.get()
        for item, (price, category) in menus[shop_name].items():
            self.menu_listbox.insert(tk.END, f"{item} - ₹{price} ({category})")

    def place_order(self):
        """Process order and save it to Excel"""
        customer_name = self.customer_entry.get().strip()
        shop_name = self.shop_var.get()
        selected_items = [self.menu_listbox.get(i).split(" - ")[0] for i in self.menu_listbox.curselection()]

        if not customer_name:
            messagebox.showerror("Error", "Enter Customer Name")
            return
        if not selected_items:
            messagebox.showerror("Error", "Select at least one item")
            return

        total_bill = sum(menus[shop_name][item][0] for item in selected_items)
        order_data = [[customer_name, shop_name, item, menus[shop_name][item][0]] for item in selected_items]

        # Save order to Excel
        try:
            existing_orders = pd.read_excel(order_file, engine="openpyxl")
            new_orders = pd.DataFrame(order_data, columns=["Customer", "Shop", "Food Item", "Price"])
            updated_orders = pd.concat([existing_orders, new_orders], ignore_index=True)
        except FileNotFoundError:
            updated_orders = pd.DataFrame(order_data, columns=["Customer", "Shop", "Food Item", "Price"])

        updated_orders.to_excel(order_file, index=False, engine="openpyxl")

        self.order_summary.config(text=f"Order Placed! Total: ₹{total_bill}")
        messagebox.showinfo("Success", f"Order placed successfully!\nTotal: ₹{total_bill}")

    def generate_bill(self):
        """Display the bill receipt for the most recent order."""
        try:
            orders = pd.read_excel(order_file, engine="openpyxl")

            if orders.empty:
                messagebox.showwarning("No Orders", "No orders placed yet!")
                return

            # Get the last order's customer and shop
            last_customer = orders.iloc[-1]["Customer"]
            last_shop = orders.iloc[-1]["Shop"]

            # Filter orders that belong to the last customer and shop (last order)
            last_order_items = orders[(orders["Customer"] == last_customer) & (orders["Shop"] == last_shop)]

            if last_order_items.empty:
                messagebox.showwarning("No Orders", "No valid orders found!")
                return

            # Construct bill details
            bill_text = f"===== BILL RECEIPT =====\nCustomer: {last_customer}\nShop: {last_shop}\n\nItems:\n"
            total_price = 0

            for _, row in last_order_items.iterrows():
                item_name = row["Food Item"]
                price = row["Price"]
                bill_text += f"- {item_name} - ₹{price}\n"
                total_price += price

            bill_text += f"\nTotal: ₹{total_price}\n========================="

            # Display bill receipt
            messagebox.showinfo("Bill Receipt", bill_text)

        except (FileNotFoundError, KeyError):
            messagebox.showwarning("Error", "No order history found!")

    def display_revenue(self):
        """Display total revenue"""
        try:
            orders = pd.read_excel(order_file, engine="openpyxl")
            total_revenue = orders["Price"].sum()
        except (FileNotFoundError, KeyError):
            total_revenue = 0

        messagebox.showinfo("Total Revenue", f"Total Revenue: ₹{total_revenue}")

    def display_customers(self):
        """Show unique customers"""
        try:
            orders = pd.read_excel(order_file, engine="openpyxl")
            unique_customers = orders["Customer"].unique()
        except (FileNotFoundError, KeyError):
            unique_customers = []

        customer_list = "\n".join(unique_customers) if unique_customers else "No customers yet."
        messagebox.showinfo("Unique Customers", f"Customers:\n{customer_list}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.mainloop()
