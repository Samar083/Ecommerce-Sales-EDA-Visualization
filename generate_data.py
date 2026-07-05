"""
Generates a realistic synthetic E-Commerce Sales dataset for
CodeAlpha Data Analytics Internship (Task 2: EDA, Task 3: Data Visualization)
"""

import numpy as np
import pandas as pd

np.random.seed(42)

n = 2000

categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Sports", "Books", "Toys"]
category_price_range = {
    "Electronics": (1500, 60000),
    "Fashion": (300, 5000),
    "Home & Kitchen": (500, 15000),
    "Beauty": (150, 3000),
    "Sports": (400, 10000),
    "Books": (100, 1200),
    "Toys": (200, 4000),
}

regions = ["North", "South", "East", "West", "Central"]
segments = ["Consumer", "Corporate", "Home Office"]
payment_modes = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"]
ship_modes = ["Standard", "Express", "Same Day"]

# date range: 2 years of daily orders
dates = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
order_dates = np.random.choice(dates, size=n)

rows = []
for i in range(n):
    category = np.random.choice(categories, p=[0.22, 0.20, 0.15, 0.13, 0.12, 0.09, 0.09])
    low, high = category_price_range[category]
    price = np.round(np.random.uniform(low, high), 2)
    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 4, 5], p=[0.35, 0.15, 0.1, 0.15, 0.1, 0.08, 0.04, 0.03])
    discount_pct = np.random.choice([0, 5, 10, 15, 20, 25, 30], p=[0.25, 0.2, 0.2, 0.15, 0.1, 0.06, 0.04])
    sales = round(price * quantity * (1 - discount_pct / 100), 2)

    # profit margin varies by category, occasionally negative (loss-making discounted orders)
    base_margin = {
        "Electronics": 0.10, "Fashion": 0.25, "Home & Kitchen": 0.18,
        "Beauty": 0.30, "Sports": 0.20, "Books": 0.15, "Toys": 0.22
    }[category]
    margin_noise = np.random.normal(0, 0.08)
    profit = round(sales * (base_margin + margin_noise - discount_pct / 300), 2)

    region = np.random.choice(regions, p=[0.22, 0.20, 0.18, 0.25, 0.15])
    segment = np.random.choice(segments, p=[0.55, 0.30, 0.15])
    payment = np.random.choice(payment_modes, p=[0.35, 0.25, 0.15, 0.15, 0.10])
    ship_mode = np.random.choice(ship_modes, p=[0.6, 0.3, 0.1])

    order_date = pd.Timestamp(order_dates[i])
    ship_delay = {"Standard": np.random.randint(3, 7), "Express": np.random.randint(1, 3), "Same Day": 0}[ship_mode]
    ship_date = order_date + pd.Timedelta(days=int(ship_delay))

    # occasional missing values to make EDA realistic
    customer_age = np.random.randint(18, 65) if np.random.rand() > 0.03 else np.nan
    rating = np.random.choice([np.nan, 1, 2, 3, 4, 5], p=[0.35, 0.03, 0.05, 0.15, 0.22, 0.20])

    rows.append({
        "Order_ID": f"ORD{10000 + i}",
        "Order_Date": order_date.date(),
        "Ship_Date": ship_date.date(),
        "Category": category,
        "Region": region,
        "Customer_Segment": segment,
        "Payment_Mode": payment,
        "Ship_Mode": ship_mode,
        "Quantity": quantity,
        "Unit_Price": price,
        "Discount_Percent": discount_pct,
        "Sales": sales,
        "Profit": profit,
        "Customer_Age": customer_age,
        "Customer_Rating": rating,
    })

df = pd.DataFrame(rows)
df.sort_values("Order_Date", inplace=True)
df.reset_index(drop=True, inplace=True)

# add a handful of duplicate rows on purpose (common real-world data issue)
dupes = df.sample(15, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

df.to_csv("/home/claude/CodeAlpha_DataAnalytics/data/ecommerce_sales.csv", index=False)
print("Dataset generated:", df.shape)
print(df.head())
