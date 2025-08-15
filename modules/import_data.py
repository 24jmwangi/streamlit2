import kagglehub
import pandas as pd
import os
import streamlit as st

@st.cache_data
def get_data():
    path = kagglehub.dataset_download("ihelon/coffee-sales")
    csv_path  = os.path.join(path, "index_1.csv")
    print("Path to dataset files:", path)
    df = pd.read_csv(csv_path)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df
