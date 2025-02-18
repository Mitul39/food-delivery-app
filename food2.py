import streamlit as st
import pandas as pd
import os

# Excel File Names
MENU_FILE = "food_menu.xlsx"
ORDER_FILE = "order_history.xlsx"

# Load Food Menu
try:
    df = pd.read_excel(MENU_FILE, engine="openpyxl")
except FileNotFoundError:
    st.error(f"File '{MENU_FILE}' not found. Please upload the menu.")
    st.stop()

# Convert Menu to Dictionary Format
menus = {}
for _, row in df.iterrows():
    shop, item, price, category = row["Shop Name"], row["Food Item"], row["Price (₹)"], row["Category"]
    if shop not in menus:
        menus[shop] = {}
    menus[shop][item] = {"price": price, "category": category}

# Ensure order file exists
if not os.path.exists(ORDER_FILE):
    pd.DataFrame(columns=["Customer", "Shop", "Food Item", "Price"]).to_excel(ORDER_FILE, index=False, engine="openpyxl")

# Initialize Session State for Order History
if "order_history" not in st.session_state:
    st.session_state.order_history = []

# Streamlit UI
st.title("🍔 Online Food Delivery System")
st.markdown("---")

# Customer Name Input
customer_name = st.text_input("Enter Customer Name")

# Shop Selection
shop_list = list(menus.keys())
shop_name = st.selectbox("🏬 Select a Shop", shop_list)

# Category Filter
categories = list(set(item["category"] for item in menus[shop_name].values()))
category_filter = st.selectbox("🔍 Filter by Category", ["All"] + categories)

# Menu Display
st.subheader(f"📜 Menu for {shop_name}")

# Filter Menu by Category
filtered_menu = {
    item: data for item, data in menus[shop_name].items()
    if category_filter == "All" or data["category"] == category_filter
}

# Item Selection
selected_items = st.multiselect("🍽️ Select food items", list(filtered_menu.keys()))

# Order Summary
if selected_items:
    st.subheader("📝 Order Summary")
    total_bill = sum(filtered_menu[item]["price"] for item in selected_items)

    for item in selected_items:
        st.write(f"- {item}: ₹{filtered_menu[item]['price']}")
    st.write(f"**Total Bill: ₹{total_bill}**")

# Place Order Button
if selected_items and st.button("✅ Confirm Order"):
    if not customer_name.strip():
        st.error("⚠️ Please enter your name!")
    else:
        order_data = [[customer_name, shop_name, item, filtered_menu[item]["price"]] for item in selected_items]

        # Load existing data and append new order
        existing_orders = pd.read_excel(ORDER_FILE, engine="openpyxl")
        updated_orders = pd.concat([existing_orders, pd.DataFrame(order_data, columns=["Customer", "Shop", "Food Item", "Price"])], ignore_index=True)
        updated_orders.to_excel(ORDER_FILE, index=False, engine="openpyxl")

        # Update Session State
        st.session_state.order_history.extend(order_data)

        st.success(f"✅ Order placed successfully! Total: ₹{total_bill}")

# View Revenue Button
if st.button("💰 View Revenue"):
    # Load order history
    orders = pd.read_excel(ORDER_FILE, engine="openpyxl")

    # Group by shop and calculate revenue
    revenue = orders.groupby("Shop")["Price"].sum().reset_index()
    revenue = revenue.rename(columns={"Price": "Total Revenue (₹)"})

    # Display the revenue
    st.subheader("📊 Revenue Report")
    st.dataframe(revenue)
