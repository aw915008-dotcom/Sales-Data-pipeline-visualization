import pandas as pd
from pymongo import MongoClient
import streamlit as st
import plotly.express as px

# ============================
# 1) Connect to MongoDB
# ============================
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "MyDatabase"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ============================
# 2) Streamlit page config
# ============================
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# ============================
# 3) Custom CSS for Dark Theme
# ============================
st.markdown(
    """
    <style>
    .stApp { 
        background-color: #1e1e2f; /* Dark gray background */
        color: #f0f0f0; 
    }
    .stTitle, .stSubheader { 
        color: #ffcc00;  /* Golden Yellow */
        font-weight: bold; 
    }
    .stMarkdown, .stText { 
        color: #e0e0e0; 
    }
    .stDataFrame th { 
        background-color: #44475a; 
        color: #ffffff; 
    }
    .stDataFrame td {
        background-color: #2b2b3c; 
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Retail Sales Dashboard (MongoDB + Streamlit)")

# ============================
# Helper: Convert numeric columns
# ============================
def convert_numeric(df, cols):
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

numeric_cols = ["TotalSpent", "TotalQuantity", "TotalRevenue"]

# ============================
# Load all dataframes
# ============================
dfs = {}
collections = [
    "TopCustomers", "BestSellingProducts", "BranchRevenueComparison",
    "MonthlySalesTrends", "SeasonalProductDemand", "StockPlanning"
]

for coll in collections:
    df = pd.DataFrame(list(db[coll].find({}, {"_id":0})))
    df = convert_numeric(df, numeric_cols)
    df.columns = df.columns.str.strip()
    if "Month" in df.columns:
        df["Month"] = pd.to_datetime(df["Month"])
    dfs[coll] = df

# ============================
# Display 3 rows of Charts (2 per row)
# ============================

# -------- Row 1 --------
col1, col2 = st.columns(2)

with col1:
    st.subheader("👑 Top Customers")
    if not dfs["TopCustomers"].empty:
        fig = px.bar(dfs["TopCustomers"], x="TotalSpent", y="CustomerName",
                     orientation="h", text="TotalSpent",
                     color="TotalSpent", color_continuous_scale=px.colors.sequential.Inferno)
        st.plotly_chart(fig, use_container_width=True, height=500)
        st.dataframe(dfs["TopCustomers"], height=300)
    else:
        st.warning("No data in TopCustomers")

with col2:
    st.subheader("🔥 Best-Selling Products")
    if not dfs["BestSellingProducts"].empty:
        fig = px.bar(dfs["BestSellingProducts"], x="ProductName", y="TotalQuantity",
                     text="TotalQuantity", color="ProductName",
                     color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig, use_container_width=True, height=500)
        st.dataframe(dfs["BestSellingProducts"], height=300)
    else:
        st.warning("No data in BestSellingProducts")

# -------- Row 2 --------
col3, col4 = st.columns(2)

with col3:
    st.subheader("🏬 Branch Revenue Comparison")
    if not dfs["BranchRevenueComparison"].empty:
        fig = px.bar(dfs["BranchRevenueComparison"], x="BranchName", y="TotalRevenue",
                     text="TotalRevenue", color="BranchName",
                     color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig, use_container_width=True, height=500)
        st.dataframe(dfs["BranchRevenueComparison"], height=300)
    else:
        st.warning("No data in BranchRevenueComparison")

with col4:
    st.subheader("📈 Monthly Sales Trends")
    if not dfs["MonthlySalesTrends"].empty:
        fig = px.line(dfs["MonthlySalesTrends"], x="Month", y="TotalRevenue",
                      markers=True, line_shape="linear",
                      color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig, use_container_width=True, height=500)
        st.dataframe(dfs["MonthlySalesTrends"], height=300)
    else:
        st.warning("No data in MonthlySalesTrends")

# -------- Row 3 --------
col5, col6 = st.columns(2)

with col5:
    st.subheader("🌸 Seasonal Product Demand")
    if not dfs["SeasonalProductDemand"].empty:
        fig = px.line(dfs["SeasonalProductDemand"], x="Month", y="TotalQuantity",
                      color="ProductName", markers=True,
                      color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig, use_container_width=True, height=500)
        st.dataframe(dfs["SeasonalProductDemand"], height=300)
    else:
        st.warning("No data in SeasonalProductDemand")

with col6:
    st.subheader("📦 Stock Planning by Branch")
    if not dfs["StockPlanning"].empty:
        fig = px.scatter(dfs["StockPlanning"], x="BranchName", y="TotalQuantity",
                         color="ProductName", size="TotalQuantity",
                         hover_name="ProductName",
                         color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True, height=500)
        st.dataframe(dfs["StockPlanning"], height=300)
    else:
        st.warning("No data in StockPlanning")

st.success("✅ Retail Sales Dashboard loaded successfully (Dark Mode)!")
