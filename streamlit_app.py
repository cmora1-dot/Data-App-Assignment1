import math
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Aggregated bar chart
st.dataframe(df.groupby("Category").sum(numeric_only=True))
st.bar_chart(
    df.groupby("Category", as_index=False).sum(numeric_only=True),
    x="Category",
    y="Sales",
    color="#04f",
)

# Calculate overall metrics across ALL products before filtering or setting index
overall_total_sales = df["Sales"].sum()
overall_total_profit = df["Profit"].sum()
overall_profit_margin = (
    (overall_total_profit / overall_total_sales) * 100
    if overall_total_sales != 0
    else 0.0
)

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index("Order_Date", inplace=True)

sales_by_month = (
    df.filter(items=["Sales"]).groupby(pd.Grouper(freq="M")).sum()
)

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# ---------------------------------------------------------
# (1) Category dropdown
# ---------------------------------------------------------
categories = sorted(df["Category"].unique().tolist())
selected_category = st.selectbox("Select Category", categories)

# Filter dataset to selected Category
cat_filtered_df = df[df["Category"] == selected_category]

# ---------------------------------------------------------
# (2) Multi-select for Sub_Category within selected Category
# ---------------------------------------------------------
# Handles either 'Sub_Category' or 'Sub-Category' column name
subcat_col = "Sub_Category" if "Sub_Category" in df.columns else "Sub-Category"
subcategories = sorted(cat_filtered_df[subcat_col].unique().tolist())

selected_subcategories = st.multiselect(
    f"Select Sub-Category items in '{selected_category}'",
    options=subcategories,
    default=subcategories,  # Pre-selects all items by default
)

# Filter dataset to selected Sub-Categories
selected_df = cat_filtered_df[cat_filtered_df[subcat_col].isin(selected_subcategories)]

# ---------------------------------------------------------
# (3) Line chart of monthly sales for selected items
# ---------------------------------------------------------
st.write("### Monthly Sales for Selected Sub-Categories")

if not selected_df.empty:
    selected_sales_by_month = selected_df.groupby(pd.Grouper(freq="M"))["Sales"].sum()
    st.line_chart(selected_sales_by_month)
else:
    st.warning("Please select at least one Sub-Category.")

# ---------------------------------------------------------
# (4) & (5) Metrics with Delta for Profit Margin
# ---------------------------------------------------------
st.write("### Key Metrics")

selected_total_sales = selected_df["Sales"].sum() if not selected_df.empty else 0.0
selected_total_profit = selected_df["Profit"].sum() if not selected_df.empty else 0.0

if selected_total_sales != 0:
    selected_profit_margin = (selected_total_profit / selected_total_sales) * 100
else:
    selected_profit_margin = 0.0

# Difference between selected selection's profit margin and overall dataset average
margin_delta = selected_profit_margin - overall_profit_margin

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Total Sales",
    value=f"${selected_total_sales:,.2f}",
)

col2.metric(
    label="Total Profit",
    value=f"${selected_total_profit:,.2f}",
)

col3.metric(
    label="Overall Profit Margin",
    value=f"{selected_profit_margin:.2f}%",
    delta=f"{margin_delta:+.2f}%",
)
