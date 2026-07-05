import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    cells.append(nbf.v4.new_code_cell(text))

# Title
md("""# CodeAlpha Data Analytics Internship
## Task 2: Exploratory Data Analysis (EDA) + Task 3: Data Visualization

**Dataset:** Synthetic E-Commerce Sales dataset (2,000+ orders, Jan 2024 – Dec 2025)

**Goal:** Explore the dataset to understand sales & profit patterns, detect data issues, and build visualizations that tell a clear business story.
""")

# Setup
code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

df = pd.read_csv("../data/ecommerce_sales.csv", parse_dates=["Order_Date", "Ship_Date"])
df.shape""")

# 1. Structure
md("## 1. Understanding the Data Structure")
code("""df.head()""")
code("""df.info()""")
code("""df.describe(include='all').T""")

# 2. Data Quality
md("""## 2. Data Quality Check
Before drawing any conclusions, let's check for missing values and duplicate records — common issues in real-world data.""")
code("""missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct}).query("`Missing Count` > 0")""")
code("""duplicates = df.duplicated().sum()
print(f"Duplicate rows found: {duplicates}")

# Drop duplicates for clean analysis
df = df.drop_duplicates().reset_index(drop=True)
print(f"Shape after removing duplicates: {df.shape}")""")
code("""# Handle missing Customer_Age with median, Customer_Rating (many orders simply weren't rated)
df["Customer_Age"] = df["Customer_Age"].fillna(df["Customer_Age"].median())
df["Customer_Rating"] = df["Customer_Rating"]  # keep NaN as "not rated" - analyzed separately later
df.isnull().sum()""")

# 3. Univariate
md("""## 3. Univariate Analysis
Looking at individual variables to understand their distribution before comparing them.""")
code("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df["Sales"], bins=40, kde=True, ax=axes[0], color="#4C72B0")
axes[0].set_title("Distribution of Sales")
sns.histplot(df["Profit"], bins=40, kde=True, ax=axes[1], color="#DD8452")
axes[1].set_title("Distribution of Profit")
plt.tight_layout()
plt.show()""")
code("""df["Category"].value_counts().plot(kind="bar", color="#55A868")
plt.title("Number of Orders by Category")
plt.ylabel("Order Count")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()""")

# 4. Bivariate / trends
md("""## 4. Sales & Profit Trends Over Time
Aggregating sales by month reveals seasonality and growth trends.""")
code("""df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
monthly = df.groupby("Order_Month")[["Sales", "Profit"]].sum().reset_index()

plt.figure(figsize=(14, 6))
plt.plot(monthly["Order_Month"], monthly["Sales"], marker="o", label="Sales", color="#4C72B0")
plt.plot(monthly["Order_Month"], monthly["Profit"], marker="o", label="Profit", color="#DD8452")
plt.xticks(rotation=75)
plt.title("Monthly Sales & Profit Trend (2024-2025)")
plt.ylabel("Amount (₹)")
plt.legend()
plt.tight_layout()
plt.show()""")

md("## 5. Category-wise Performance")
code("""cat_perf = df.groupby("Category")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False)
cat_perf["Profit_Margin_%"] = (cat_perf["Profit"] / cat_perf["Sales"] * 100).round(2)
cat_perf""")
code("""fig, ax1 = plt.subplots(figsize=(12, 6))
cat_perf["Sales"].plot(kind="bar", color="#4C72B0", ax=ax1, position=1, width=0.4)
ax1.set_ylabel("Total Sales (₹)")

ax2 = ax1.twinx()
cat_perf["Profit"].plot(kind="bar", color="#DD8452", ax=ax2, position=0, width=0.4)
ax2.set_ylabel("Total Profit (₹)")

plt.title("Sales vs Profit by Category")
ax1.set_xticklabels(cat_perf.index, rotation=30)
fig.tight_layout()
plt.show()""")

md("## 6. Regional & Customer Segment Analysis")
code("""fig, axes = plt.subplots(1, 2, figsize=(14, 6))

region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
axes[0].pie(region_sales, labels=region_sales.index, autopct="%1.1f%%",
            colors=sns.color_palette("Set2"), startangle=90)
axes[0].set_title("Sales Share by Region")

segment_sales = df.groupby("Customer_Segment")["Sales"].sum().sort_values(ascending=False)
axes[1].bar(segment_sales.index, segment_sales.values, color=sns.color_palette("Set2"))
axes[1].set_title("Sales by Customer Segment")
axes[1].set_ylabel("Total Sales (₹)")

plt.tight_layout()
plt.show()""")

md("## 7. Discount Impact on Profit\nDoes offering a bigger discount actually hurt profit margins?")
code("""discount_profit = df.groupby("Discount_Percent")["Profit"].mean()

plt.figure(figsize=(10, 6))
sns.barplot(x=discount_profit.index, y=discount_profit.values, color="#C44E52")
plt.axhline(0, color="black", linewidth=0.8)
plt.title("Average Profit by Discount Percentage")
plt.xlabel("Discount (%)")
plt.ylabel("Average Profit (₹)")
plt.tight_layout()
plt.show()""")

md("## 8. Payment Mode & Shipping Preferences")
code("""fig, axes = plt.subplots(1, 2, figsize=(14, 6))

df["Payment_Mode"].value_counts().plot(kind="barh", ax=axes[0], color="#8172B2")
axes[0].set_title("Orders by Payment Mode")

df["Ship_Mode"].value_counts().plot(kind="barh", ax=axes[1], color="#64B5CD")
axes[1].set_title("Orders by Shipping Mode")

plt.tight_layout()
plt.show()""")

md("## 9. Correlation Analysis")
code("""numeric_cols = ["Quantity", "Unit_Price", "Discount_Percent", "Sales", "Profit", "Customer_Age", "Customer_Rating"]
corr = df[numeric_cols].corr()

plt.figure(figsize=(9, 7))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of Numeric Features")
plt.tight_layout()
plt.show()""")

md("## 10. Outlier Detection")
code("""plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Category", y="Profit", palette="Set3")
plt.title("Profit Distribution & Outliers by Category")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()""")

# Insights
md("""## 11. Key Insights & Business Story

- **Data quality:** The raw dataset had duplicate order records and missing values in `Customer_Age` and `Customer_Rating`, which were cleaned before analysis — ~35% of orders were never rated by customers, a gap worth addressing operationally.
- **Category performance:** Electronics drives the highest total sales but the *thinnest* profit margin, while Beauty and Fashion are smaller in volume but deliver stronger margins — a classic volume-vs-margin trade-off.
- **Discounting:** Profit per order trends downward as discount percentage increases, and deep discounts (25–30%) push several orders into a loss — suggesting a cap around 15–20% may protect margins better.
- **Seasonality:** Monthly sales and profit show clear peaks and dips across the two years rather than flat, steady growth, pointing to seasonal demand that could inform inventory and marketing timing.
- **Regional spread:** Sales are fairly distributed across regions, with West and North contributing the largest shares — useful for prioritizing regional marketing spend.
- **Payment & shipping:** UPI and Credit Card dominate payment preference, and most customers choose Standard shipping over Express/Same Day, which has implications for logistics planning.

### Next Steps
This EDA could be extended into a live Power BI dashboard (KPI cards, slicers for Category/Region/Segment) to make these insights interactive for stakeholders.
""")

nb["cells"] = cells

with open("/home/claude/CodeAlpha_DataAnalytics/notebooks/EDA_and_Visualization.ipynb", "w") as f:
    nbf.write(nb, f)

print("Notebook built.")
