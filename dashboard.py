import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("🇧🇷 Brazil ↔ Canada Trade Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("brazil_trade_summary.csv")


df = load_data()

# pivot para gráfico
pivot = df.pivot(index="date", columns="trade_type", values="Value")

st.subheader("Import vs Export")

st.line_chart(pivot)
