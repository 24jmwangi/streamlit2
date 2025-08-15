import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go 


@st.cache_data
def plots(filtered_df):
    # Sales Trend
    st.subheader("Sales Trend")
    sales_trend = filtered_df.groupby(filtered_df["datetime"].dt.date)["money"].sum()
    st.line_chart(sales_trend)

    # Heatmap visualize sales volume by day of week and hour to spot peak times

    st.subheader("Sales Volume by Day of Week and Hour")    
    filtered_df["hour"] = filtered_df["datetime"].dt.hour      
    filtered_df["day_of_week"] = filtered_df["datetime"].dt.day_name()
    # Order days for better readability
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = (
        filtered_df.groupby(["day_of_week", "hour"])["money"]
        .sum()
        .unstack()
        .reindex(days_order)
    )

    fig, ax = plt.subplots(figsize=(10, 4))
    cax = ax.imshow(heatmap_data, aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns)
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)
    plt.xlabel("Hour of Day")
    plt.ylabel("Day of Week")
    plt.title("Sales Volume Heatmap")
    fig.colorbar(cax, ax=ax, label="Total Sales")
    st.pyplot(fig)

    # Treemap: visualize sales by coffee type and payment type
    st.subheader("Sales by Coffee Type")
    treemap_df = (
        filtered_df.groupby(["cash_type", "coffee_name"], as_index=False)["money"].sum()
    )
    fig = px.treemap(
        treemap_df,
        path=["cash_type", "coffee_name"],
        values="money",
        color="coffee_name",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Sankey chart: visualize flow from payment type to coffee name
    st.subheader("Sales Flow: Payment Type → Coffee Name")
    sankey_df = (
        filtered_df.groupby(["cash_type", "coffee_name"], as_index=False)["money"].sum()
    )

    # Prepare labels
    payment_types = sankey_df["cash_type"].unique().tolist()
    coffee_names = sankey_df["coffee_name"].unique().tolist()
    labels = payment_types + coffee_names

    # Prepare source and target indices
    source = sankey_df["cash_type"].apply(lambda x: labels.index(x))
    target = sankey_df["coffee_name"].apply(lambda x: labels.index(x))
    value = sankey_df["money"]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=10,
            thickness=30,
            line=dict(color="yellow", width=0.5),
            label=labels,
            # color="",
       

        ),
        link=dict(
            source=source,
            target=target,
            value=value
        ))])
    fig.update_layout(
        font=dict(color="black",
        size=12)
        )
    st.plotly_chart(fig, use_container_width=True)



    # Area chart for coffee type sales
    st.subheader("Coffee Type Sales Over Time")
    area_data = (
        filtered_df.groupby([filtered_df["datetime"].dt.date, "coffee_name"])["money"]
        .sum()
        .unstack(fill_value=0)
        .sort_index()
    )
    st.area_chart(area_data, use_container_width=True)
    st.subheader("Dataframe")
    st.dataframe(filtered_df.head(10)) 


  
