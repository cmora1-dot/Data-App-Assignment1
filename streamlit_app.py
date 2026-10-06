import math
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.title("Data App Assignment, on July 14th")[cite: 1, 3]

st.write("### Input Data and Examples")[cite: 1, 3]
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)[cite: 1, 3]
st.dataframe(df)[cite: 1, 3]

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")[cite: 1, 3]

# Aggregated bar chart
st.dataframe(df.groupby("Category").sum(numeric_only=True))[cite: 1, 3]
st.bar_chart(
    df.groupby("Category", as_index=False).sum(numeric_only=True),
    x="Category",
    y="Sales",
    color="#04f",
)[cite: 1, 3]

# Calculate overall metrics across ALL products before filtering or setting index
overall_total_sales = df["Sales"].sum()
overall_total_profit = df["Profit"].sum()
overall_profit_margin = (
    (overall_total_profit / overall_total_sales) * 100
    if overall_total_sales != 0
    else 0.0
)

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])[cite: 1, 3]
df.set_index("Order_Date", inplace=True)[cite: 1, 3]

# Changed freq="M" to freq="ME" to prevent Pandas ValueError
sales_by_month = (
    df.filter(items=["Sales"]).groupby(pd.Grouper(freq="ME")).sum()
)

st.dataframe(sales_by_month)[cite: 1, 3]
st.line_chart(sales_by_month, y="Sales")[cite: 1, 3]

st.write("## Your additions")[cite: 1, 3]

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
subcat_col = "Sub_Category" if "Sub_Category" in df.columns else "Sub-Category"
subcategories = sorted(cat_filtered_df[subcat_col].unique().tolist())

selected_subcategories = st.multiselect(
    f"Select Sub-Category items in '{selected_category}'",
    options=subcategories,
    default=subcategories,
)

# Filter dataset to selected Sub-Categories
selected_df = cat_filtered_df[cat_filtered_df[subcat_col].isin(selected_subcategories)]

# ---------------------------------------------------------
# (3) Line chart of monthly sales for selected items
# ---------------------------------------------------------
st.write("### Monthly Sales for Selected Sub-Categories")

if not selected_df.empty:
    selected_sales_by_month = selected_df.groupby(pd.Grouper(freq="ME"))["Sales"].sum()
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
