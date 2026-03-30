import streamlit as st
import pandas as pd

from src.download_data import download_data
from src.process_data import process_data

# Configuração
st.set_page_config(layout="wide")

st.title("🇧🇷 Brazil ↔ Canada Trade Dashboard")

# Cache pesado
@st.cache_data
def load_data():
    df_raw = download_data()
    df = process_data(df_raw)
    return df

df = load_data()

# Ordenar
df = df.sort_values("date")

# Pivot
pivot = (
    df.pivot(index="date", columns="trade_type", values="Value")
    .fillna(0)
)

# Garantir colunas
for col in ["Import", "Export"]:
    if col not in pivot.columns:
        pivot[col] = 0

pivot = pivot[sorted(pivot.columns)]

# ======================
# GRÁFICO
# ======================

st.subheader("📈 Import vs Export Over Time")
st.line_chart(pivot)

# ======================
# KPIs
# ======================

col1, col2 = st.columns(2)

total_import = df[df["trade_type"] == "Import"]["Value"].sum()
total_export = df[df["trade_type"] == "Export"]["Value"].sum()

with col1:
    st.metric("Total Imports", f"${total_import:,.0f}")

with col2:
    st.metric("Total Exports", f"${total_export:,.0f}")
