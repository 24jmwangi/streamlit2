import streamlit as st
import datetime
import pandas as pd


def ui(data):

    st.set_page_config(page_title="☕ Coffee Sales Dashboard", layout="wide")

    # Create filters
    payment_type = st.sidebar.multiselect("Select Payment Type",
    options=data["cash_type"].unique(), default=data["cash_type"].unique())

    coffee_name = st.sidebar.multiselect("Select Coffee Name",
    options=data["coffee_name"].unique(), default=data["coffee_name"].unique())
    min_date = data["datetime"].min().date()
    max_date = data["datetime"].max().date()

    preset = st.sidebar.selectbox(
        "Quick Date Ranges",
        ["Custom", "This Week", "This Month", "Last 3 Months", "Last 6 Months", "This Year"]
    )
    today = max_date
    if preset == "This Week":
        start = today - datetime.timedelta(days=today.weekday())
        end = today
    elif preset == "This Month":
        start = today.replace(day=1)
        end = today
    elif preset == "Last 3 Months":
        start = (today - pd.DateOffset(months=3)).date()
        end = today
    elif preset == "Last 6 Months":
        start = (today - pd.DateOffset(months=6)).date()
        end = today
    elif preset == "This Year":
        start = today.replace(month=1, day=1)
        end = today
    else:  # Custom
        date_input = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if not isinstance(date_input, tuple) or len(date_input) != 2:
            st.warning("Please select a valid start and end date.")
            st.stop()
        start, end = date_input


    # Filter data based on selection
    filtered_df = data[
        (data["cash_type"].isin(payment_type)) & 
        (data["coffee_name"].isin(coffee_name)) & 
        (data["datetime"].dt.date >= start) & 
        (data["datetime"].dt.date <= end)
    ]
    if filtered_df.empty:
        st.warning("No data found for the selected filters.")
        st.stop()
    
    # Sidebar sumarries
    st.sidebar.title("Summaries")
    
    st.sidebar.metric("💰 Total Sales", filtered_df["money"].sum().round(1))
    st.sidebar.metric("📊 Average Sales", filtered_df["money"].mean().round(1))
    st.sidebar.metric("🧾Total Transactions", filtered_df["datetime"].nunique())
    st.sidebar.metric("☕ Coffee Types", filtered_df["coffee_name"].nunique())

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Sales", filtered_df["money"].sum().round(1))
    with col2:
        st.metric("📊 Average Sales", filtered_df["money"].mean().round(1))
    with col3:
        st.metric("🧾Total Transactions", filtered_df["datetime"].nunique())
    with col4:
        st.metric("☕ Coffee Types", filtered_df["coffee_name"].nunique())
  
    
    return filtered_df