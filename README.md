# CodeAlpha_DataAnalytics

📊 **CodeAlpha Data Analytics Internship Project**
Tasks Completed: **Task 2 – Exploratory Data Analysis (EDA)** & **Task 3 – Data Visualization**

## 📁 Project Overview

This project analyzes a synthetic **E-Commerce Sales dataset** (2,000+ orders across Jan 2024 – Dec 2025) to uncover sales, profit, and customer behavior trends. It combines exploratory data analysis with a range of visualizations to turn raw transactional data into clear, decision-ready insights.

## 🗂 Repository Structure

```
CodeAlpha_DataAnalytics/
├── data/
│   └── ecommerce_sales.csv          # Dataset used for analysis
├── notebooks/
│   └── EDA_and_Visualization.ipynb  # Full analysis notebook (executed, with charts)
├── generate_data.py                 # Script used to generate the dataset
├── requirements.txt
└── README.md
```

## 🛠 Tools & Libraries

- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Jupyter Notebook

## 🔍 What's Inside the Notebook

1. Data structure exploration (`info()`, `describe()`)
2. Data quality checks — missing values & duplicate detection/cleaning
3. Univariate analysis of Sales and Profit distributions
4. Monthly Sales & Profit trend analysis
5. Category-wise performance (Sales vs Profit vs Margin)
6. Regional and Customer Segment breakdowns
7. Discount % impact on average profit
8. Payment mode & shipping mode preferences
9. Correlation heatmap of numeric features
10. Outlier detection via boxplots
11. Key business insights & recommendations

## 📌 Key Insights

- Electronics drives the highest sales volume but has the thinnest profit margin, while Beauty and Fashion deliver stronger margins on lower volume.
- Profit per order declines as discount percentage rises, with 25–30% discounts pushing several orders into a loss.
- Sales and profit show clear month-to-month seasonality rather than flat growth.
- West and North regions contribute the largest share of total sales.
- UPI and Credit Card are the most preferred payment modes; Standard shipping is chosen far more often than Express or Same Day.

## ▶️ How to Run

```bash
pip install -r requirements.txt
jupyter notebook notebooks/EDA_and_Visualization.ipynb
```

## 🎓 About

Completed as part of the **CodeAlpha Data Analytics Internship**.

---
*This project is part of my Data Analyst portfolio, alongside my [Whirlpool Sales Dashboard](https://github.com/Samar083/whirlpool-sales-dashboard) built in Power BI.*
