import streamlit as st
import pandas as pd
import os

# Excel File Names
menu_file = "food_menu.xlsx"
order_file = "order_history.xlsx"

# Load Food Menu
if os.path.exists(menu_file):
    df = pd.read_excel(menu_file, engine="openpyxl")
    menus = {}
    for _, row in df.iterrows():
        shop, item, price, category = row["Shop Name"], row["Food Item"], row["Price (₹)"], row["Category"]
        if shop not in menus:
            menus[shop] = {}
        menus[shop][item] = (price, category)
else:
    st.error(f"File '{menu_file}' not found.")
    st.stop()

# Streamlit App UI
st.title("🍔 Online Food Delivery System")
st.markdown("---")

# Customer Name Input
customer_name = st.text_input("Enter Customer Name")

# Shop Selection
shop_list = list(menus.keys())
shop_name = st.selectbox("Select a Shop", shop_list)

# Menu Display
st.subheader(f"📜 Menu for {shop_name}")
menu_items = menus[shop_name]
selected_items = st.multiselect("Select food items", list(menu_items.keys()))

# Place Order Button
if st.button("🛒 Place Order"):
    if not customer_name.strip():
        st.error("Please enter your name!")
    elif not selected_items:
        st.error("Select at least one item!")
    else:
        total_bill = sum(menu_items[item][0] for item in selected_items)
        order_data = [[customer_name, shop_name, item, menu_items[item][0]] for item in selected_items]

        # Save to Excel
        if os.path.exists(order_file):
            existing_orders = pd.read_excel(order_file, engine="openpyxl")
            new_orders = pd.DataFrame(order_data, columns=["Customer", "Shop", "Food Item", "Price"])
            updated_orders = pd.concat([existing_orders, new_orders], ignore_index=True)
        else:
            updated_orders = pd.DataFrame(order_data, columns=["Customer", "Shop", "Food Item", "Price"])

        updated_orders.to_excel(order_file, index=False, engine="openpyxl")

        st.success(f"✅ Order placed successfully! Total: ₹{total_bill}")

# Generate Bill
if st.button("📄 Generate Bill"):
    if os.path.exists(order_file):
        orders = pd.read_excel(order_file, engine="openpyxl")

        if not orders.empty:
            last_customer = orders.iloc[-1]["Customer"]
            last_shop = orders.iloc[-1]["Shop"]
            last_order = orders[(orders["Customer"] == last_customer) & (orders["Shop"] == last_shop)]

            bill_text = f"### 🧾 Bill Receipt\n**Customer:** {last_customer}\n**Shop:** {last_shop}\n\n**Items:**\n"
            total_price = 0

            for _, row in last_order.iterrows():
                item_name, price = row["Food Item"], row["Price"]
                bill_text += f"- {item_name}: ₹{price}\n"
                total_price += price

            bill_text += f"\n**Total: ₹{total_price}**"
            st.markdown(bill_text)
        else:
            st.warning("No orders placed yet!")
    else:
        st.warning("No order history found!")

# View Revenue
if st.button("💰 View Revenue"):
    if os.path.exists(order_file):
        orders = pd.read_excel(order_file, engine="openpyxl")
        total_revenue = orders["Price"].sum()
        st.info(f"Total Revenue: ₹{total_revenue}")
    else:
        st.warning("No revenue data available.")

# View Customers
if st.button("🧑‍🤝‍🧑 View Customers"):
    if os.path.exists(order_file):
        orders = pd.read_excel(order_file, engine="openpyxl")
        customers = orders["Customer"].unique()
        st.write("**Unique Customers:**")
        st.write(customers if len(customers) > 0 else "No customers yet.")
    else:
        st.warning("No customer data available.")

