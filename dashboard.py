import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(layout="wide")

st.title("🇧🇷 Brazil ↔ Canada Trade Dashboard")

# Cache para performance
@st.cache_data
def load_data():
    df = pd.read_csv("brazil_trade_summary.csv")
    
    # Garantir que a data está no formato correto
    df["date"] = pd.to_datetime(df["date"])
    
    return df

df = load_data()

# Ordenar por data
df = df.sort_values("date")

# Criar pivot com proteção contra valores faltantes
pivot = (
    df.pivot(index="date", columns="trade_type", values="Value")
    .fillna(0)
)

# Garantir que colunas sempre existam
for col in ["Import", "Export"]:
    if col not in pivot.columns:
        pivot[col] = 0

# Ordenar colunas
pivot = pivot[sorted(pivot.columns)]

st.subheader("📈 Import vs Export Over Time")

st.line_chart(pivot)

# ===============
# KPIs simples
# ===============

col1, col2 = st.columns(2)

total_import = df[df["trade_type"] == "Import"]["Value"].sum()
total_export = df[df["trade_type"] == "Export"]["Value"].sum()

with col1:
    st.metric("Total Imports", f"${total_import:,.0f}")

with col2:
    st.metric("Total Exports", f"${total_export:,.0f}")
