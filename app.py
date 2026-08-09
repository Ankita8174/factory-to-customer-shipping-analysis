import pandas as pd
import streamlit as st

# Page setup
st.set_page_config(
    page_title="Factory to Customer Analysis",
    page_icon="🚚",
    layout="wide"
)

# Load dataset
df = pd.read_csv("data/orders.csv")

df.columns = df.columns.str.strip()

# Title
st.title("🚚 Factory to Customer Shipping Route Efficiency Analysis")

st.write(
    "Analysis of orders, factories, sales and shipping performance."
)

# Delivery Days
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Delivery Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

average_delivery = df["Delivery Days"].mean()

# KPIs
total_orders = len(df)
total_sales = df["Sales"].sum()
total_quantity = df["Quantity"].sum()
total_factories = df["Factory"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Orders", total_orders)
col2.metric("Total Sales", f"${total_sales:,.0f}")
col3.metric("Total Quantity", total_quantity)
col4.metric("Factories", total_factories)
col5.metric("Avg Delivery Days", f"{average_delivery:.1f}")

# Dataset
st.subheader("📋 Order Dataset")
st.dataframe(df, use_container_width=True)

# Factory-wise Sales
st.subheader("🏭 Factory-wise Sales")

factory_sales = (
    df.groupby("Factory")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(factory_sales)

# Product-wise Sales
st.subheader("🍫 Product-wise Sales")

product_sales = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_sales)

# Shipping Route Analysis
st.subheader("🚚 Shipping Route Analysis")

route_analysis = df.groupby(
    ["Factory", "Ship Mode"]
).agg(
    Total_Orders=("Order ID", "count"),
    Total_Quantity=("Quantity", "sum"),
    Total_Sales=("Sales", "sum"),
    Average_Delivery_Days=("Delivery Days", "mean")
).reset_index()

route_analysis["Average_Delivery_Days"] = route_analysis[
    "Average_Delivery_Days"
].round(2)

st.dataframe(route_analysis, use_container_width=True)

# Sales chart
st.subheader("📊 Sales by Factory")

factory_sales = df.groupby("Factory")["Sales"].sum()

st.bar_chart(factory_sales)
# Factory Performance Analysis
st.subheader("🏭 Factory Performance Analysis")

factory_analysis = df.groupby("Factory").agg(
    Total_Orders=("Order ID", "count"),
    Total_Quantity=("Quantity", "sum"),
    Total_Sales=("Sales", "sum"),
    Average_Delivery_Days=("Delivery Days", "mean")
).reset_index()

factory_analysis["Average_Delivery_Days"] = factory_analysis[
    "Average_Delivery_Days"
].round(2)

st.dataframe(factory_analysis, use_container_width=True)
# Product Analysis
st.subheader("🍫 Product Analysis")

product_analysis = df.groupby("Product Name").agg(
    Total_Orders=("Order ID", "count"),
    Total_Quantity=("Quantity", "sum"),
    Total_Sales=("Sales", "sum")
).reset_index()

product_analysis = product_analysis.sort_values(
    "Total_Sales",
    ascending=False
)

st.dataframe(product_analysis, use_container_width=True)
# Ship Mode Analysis
st.subheader("🚚 Ship Mode Analysis")

ship_mode_analysis = df.groupby("Ship Mode").agg(
    Total_Orders=("Order ID", "count"),
    Total_Quantity=("Quantity", "sum"),
    Total_Sales=("Sales", "sum"),
    Average_Delivery_Days=("Delivery Days", "mean")
).reset_index()

ship_mode_analysis["Average_Delivery_Days"] = (
    ship_mode_analysis["Average_Delivery_Days"].round(2)
)

st.dataframe(ship_mode_analysis, use_container_width=True)
# Filters
st.subheader("🔎 Dashboard Filters")

col1, col2, col3 = st.columns(3)

with col1:
    selected_factory = st.multiselect(
        "Select Factory",
        options=sorted(df["Factory"].dropna().unique()),
        default=sorted(df["Factory"].dropna().unique())
    )

with col2:
    selected_ship_mode = st.multiselect(
        "Select Ship Mode",
        options=sorted(df["Ship Mode"].dropna().unique()),
        default=sorted(df["Ship Mode"].dropna().unique())
    )

with col3:
    selected_product = st.multiselect(
        "Select Product",
        options=sorted(df["Product Name"].dropna().unique()),
        default=sorted(df["Product Name"].dropna().unique())
    )
    # Apply Filters
filtered_df = df[
    df["Factory"].isin(selected_factory) &
    df["Ship Mode"].isin(selected_ship_mode) &
    df["Product Name"].isin(selected_product)
]

st.subheader("📋 Filtered Data")
st.dataframe(filtered_df, use_container_width=True)

st.write(
    f"Showing {len(filtered_df)} orders out of {len(df)} total orders."
)
# Filtered KPI Metrics
st.subheader("📌 Filtered Summary")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "📦 Total Orders",
        filtered_df["Order ID"].nunique()
    )

with kpi2:
    st.metric(
        "💰 Total Sales",
        f"${filtered_df['Sales'].sum():,.2f}"
    )

with kpi3:
    st.metric(
        "📊 Total Quantity",
        filtered_df["Quantity"].sum()
    )

with kpi4:
    st.metric(
        "⏱️ Avg Delivery Days",
        f"{filtered_df['Delivery Days'].mean():.2f}"
    )
    # Project Conclusion
st.subheader("📝 Project Conclusion")

st.write("""
This dashboard analyzes the efficiency of the factory-to-customer
shipping process for the Nassau Candy Distributor.

The analysis helps identify:
• Factory-wise sales and order performance
• Product-wise sales and quantity
• Shipping mode performance
• Average delivery time
• High-performing factories and products
• The impact of different filters on business performance

The dashboard can help management make better decisions regarding
factory performance, product demand, and shipping operations.
""")
# Key Business Insights
st.subheader("💡 Key Business Insights")

best_factory = df.groupby("Factory")["Sales"].sum().idxmax()
best_product = df.groupby("Product Name")["Sales"].sum().idxmax()
best_ship_mode = df.groupby("Ship Mode")["Sales"].sum().idxmax()

avg_delivery = df["Delivery Days"].mean()

col1, col2 = st.columns(2)

with col1:
    st.info(f"🏭 Best Performing Factory: {best_factory}")
    st.info(f"🍫 Top Selling Product: {best_product}")

with col2:
    st.info(f"🚚 Highest Sales Ship Mode: {best_ship_mode}")
    st.info(f"⏱️ Average Delivery Time: {avg_delivery:.2f} days")

# Sales by Ship Mode
st.subheader("📊 Sales by Ship Mode")

ship_mode_sales = df.groupby("Ship Mode")["Sales"].sum()

st.bar_chart(ship_mode_sales)

# Product Sales Chart
st.subheader("📊 Sales by Product")

product_sales = df.groupby("Product Name")["Sales"].sum().sort_values(
    ascending=False
)

st.bar_chart(product_sales)

# Factory Sales Comparison
st.subheader("💰 Factory Sales Comparison")

factory_sales = df.groupby("Factory")["Sales"].sum()

st.bar_chart(factory_sales)

# Route Efficiency Score
st.subheader("⭐ Route Efficiency Score")

route_analysis["Route Efficiency Score"] = (
    100 / (1 + route_analysis["Average_Delivery_Days"])
).round(2)

st.dataframe(
    route_analysis.sort_values(
        "Route Efficiency Score",
        ascending=False
    ),
    use_container_width=True
)