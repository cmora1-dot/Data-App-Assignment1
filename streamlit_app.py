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

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum(numeric_only=True))
# Using as_index=False here preserves the Category as a column. If we exclude that, Category would become the dataframe index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(
    df.groupby("Category", as_index=False).sum(numeric_only=True),
    x="Category",
    y="Sales",
    color="#04f",
)

# Aggregating by time
# Calculate overall metrics prior to setting index (for requirement 5)
overall_total_sales = df["Sales"].sum()
overall_total_profit = df["Profit"].sum()
overall_profit_margin = (
    (overall_total_profit / overall_total_sales) * 100
    if overall_total_sales != 0
    else 0.0
)

# Here we ensure Order_Date is in datetime format, then set it as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index("Order_Date", inplace=True)

# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = (
    df.filter(items=["Sales"]).groupby(pd.Grouper(freq="M")).sum()
)

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# ---------------------------------------------------------
# (1) Category dropdown
# ---------------------------------------------------------
categories = sorted(df["Category"].unique())
selected_category = st.selectbox("Select a Category", categories)

# ---------------------------------------------------------
# (2) Multi-select for Sub_Category within selected Category
# ---------------------------------------------------------
# Dynamically check column name (handles 'Sub_Category' or 'Sub-Category')
subcat_col = "Sub_Category" if "Sub_Category" in df.columns else "Sub-Category"

cat_filtered_df = df[df["Category"] == selected_category]
subcategories = sorted(cat_filtered_df[subcat_col].unique())

selected_subcategories = st.multiselect(
    f"Select Sub-Categories in '{selected_category}'",
    options=subcategories,
    default=subcategories,
)

# Filter dataframe based on multi-select choices
selected_df = cat_filtered_df[cat_filtered_df[subcat_col].isin(selected_subcategories)]

# ---------------------------------------------------------
# (3) Line chart of monthly sales for selected items
# ---------------------------------------------------------
st.write("### Monthly Sales for Selected Items")

if not selected_df.empty:
    selected_sales_by_month = selected_df.groupby(pd.Grouper(freq="M"))[
        "Sales"
    ].sum()
    st.line_chart(selected_sales_by_month)
else:
    st.info("Please select at least one sub-category to view the line chart.")

# ---------------------------------------------------------
# (4) & (5) Metrics: Total Sales, Total Profit, and Profit Margin with Delta
# ---------------------------------------------------------
st.write("### Metrics for Selected Items")

selected_total_sales = selected_df["Sales"].sum()
selected_total_profit = selected_df["Profit"].sum()

if selected_total_sales != 0:
    selected_profit_margin = (
        selected_total_profit / selected_total_sales
    ) * 100
else:
    selected_profit_margin = 0.0

# Difference relative to overall average profit margin across all categories
margin_delta = selected_profit_margin - overall_profit_margin

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${selected_total_sales:,.2f}")
col2.metric("Total Profit", f"${selected_profit_profit:,.2f}" if 'selected_profit_profit' in locals() else f"${selected_total_profit:,.2f}")
col3.metric(
    "Overall Profit Margin",
    f"{selected_profit_margin:.2f}%",
    delta=f"{margin_delta:+.2f}%",
)