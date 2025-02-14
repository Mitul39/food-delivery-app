import pandas as pd

# Food Menu Dictionary
menus = {
    "Danny's": {
        "Pizza": (220, "Italian"),
        "Toast": (100, "Mexican"),
        "Maggie": (60, "Fast Food"),
        "Fries": (90, "French"),
        "Coffee": (25, "Beverage")
    },
    "Sweat-spot": {
        "Thepla": (30, "Desi"),
        "Pizza": (170, "Fast Food"),
        "Burger": (100, "Fast Food"),
        "Hot Chocolate": (50, "Beverage"),
        "Salad": (120, "Healthy")
    },
    "Yogi": {
        "Sandwich": (120, "Snack"),
        "Puff": (25, "Fast Food"),
        "Coco": (40, "Beverage"),
        "Juice": (60, "Beverage")
    },
}

# Convert Data to List
data = []
for shop, items in menus.items():
    for item, (price, category) in items.items():
        data.append([shop, item, price, category])

# Create DataFrame
df = pd.DataFrame(data, columns=["Shop Name", "Food Item", "Price (₹)", "Category"])

# Save to Excel
file_name = "food_menu.xlsx"
df.to_excel(file_name, index=False, engine="openpyxl")

print(f"Excel file '{file_name}' created successfully!")
