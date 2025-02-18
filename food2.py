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
        # Prepare order data
        order_data = [[customer_name, shop_name, item, filtered_menu[item]["price"]] for item in selected_items]

        # Check if the order history file exists, otherwise create it
        if os.path.exists(ORDER_FILE):
            # If file exists, load it
            orders = pd.read_excel(ORDER_FILE, engine="openpyxl")
        else:
            # If file doesn't exist, create an empty dataframe
            orders = pd.DataFrame(columns=["Customer", "Shop", "Food Item", "Price"])

        # Append the new order to the existing orders
        updated_orders = pd.concat([orders, pd.DataFrame(order_data, columns=["Customer", "Shop", "Food Item", "Price"])], ignore_index=True)

        # Save the updated orders back to the Excel file
        updated_orders.to_excel(ORDER_FILE, index=False, engine="openpyxl")

        # Update Session State
        st.session_state.order_history.extend(order_data)

        # Show Success
        st.success(f"✅ Order placed successfully! Total: ₹{total_bill}")

# Order Actions Section
st.markdown("---")
st.subheader("📦 Order Actions")

col1, col2, col3 = st.columns(3)

# Generate Bill
with col1:
    if st.button("📄 Generate Bill"):
        try:
            orders = pd.read_excel(ORDER_FILE, engine="openpyxl")
            last_order = orders[(orders["Customer"] == customer_name) & (orders["Shop"] == shop_name)].tail(len(selected_items))

            if not last_order.empty:
                bill_text = f"### 🧾 Bill Receipt\n**Customer:** {customer_name}\n\n**Shop:** {shop_name}\n\n**Items:**\n"
                total_price = 0

                for _, row in last_order.iterrows():
                    item_name, price = row["Food Item"], row["Price"]
                    bill_text += f"- {item_name}: ₹{price}\n"
                    total_price += price

                bill_text += f"\n**Total: ₹{total_price}**"
                st.markdown(bill_text)
            else:
                st.warning("⚠️ No recent orders found for this customer.")
        except FileNotFoundError:
            st.warning("⚠️ No order history found!")

# Clear Orders
with col2:
    if st.button("🗑️ Clear Orders"):
        if os.path.exists(ORDER_FILE):
            os.remove(ORDER_FILE)
            st.session_state.order_history = []
            st.success("✅ All orders have been cleared!")
        else:
            st.warning("⚠️ No orders to clear.")

# View Revenue
with col3:
    if st.button("💰 View Revenue"):
        try:
            orders = pd.read_excel(ORDER_FILE, engine="openpyxl")
            total_revenue = orders["Price"].sum()
            st.info(f"💰 Total Revenue: ₹{total_revenue}")
        except FileNotFoundError:
            st.warning("⚠️ No revenue data available.")

# Customer List
if st.button("🧑‍🤝‍🧑 View Customers"):
    try:
        orders = pd.read_excel(ORDER_FILE, engine="openpyxl")
        customers = orders["Customer"].unique()
        st.write("👤 **Unique Customers:**")
        st.write(customers if len(customers) > 0 else "No customers yet.")
    except FileNotFoundError:
        st.warning("⚠️ No customer data available.")
