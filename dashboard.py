import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Canada Trade Dashboard 🇨🇦")

@st.cache_data
def load_data():
    url = "https://huggingface.co/datasets/WilgnerCH/canada-trade-data/resolve/main/canada_trade_full.csv.gz"
    return pd.read_csv(url)


df = load_data()

# processar leve no front (temporário)
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df = df.dropna(subset=["Value"])

df_country = (
    df.groupby(["date", "Country", "trade_type"])["Value"]
    .sum()
    .reset_index()
)

# filtro
country = st.selectbox("Select Country", df_country["Country"].unique())

filtered = df_country[df_country["Country"] == country]

# pivot para gráfico
pivot = filtered.pivot(index="date", columns="trade_type", values="Value")

st.line_chart(pivot)
