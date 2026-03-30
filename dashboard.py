import streamlit as st
import pandas as pd
import altair as alt

from src.download_data import download_data
from src.process_data import process_data

# ======================
# CONFIG
# ======================
st.set_page_config(layout="wide")

st.title("🇧🇷 Brazil ↔ Canada Trade Dashboard")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df_raw = download_data()
    df = process_data(df_raw)
    return df

df = load_data()

# ======================
# PREP DATA
# ======================
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Pivot (gráfico principal)
pivot = (
    df.pivot(index="date", columns="trade_type", values="Value")
    .fillna(0)
)

for col in ["Import", "Export"]:
    if col not in pivot.columns:
        pivot[col] = 0

pivot = pivot[sorted(pivot.columns)]

# ======================
# LINE CHART (ORIGINAL)
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

# ======================
# MoM (VERSÃO MELHORADA)
# ======================
st.subheader("📊 Month-over-Month Change")

df_mom = df.copy()
df_mom = df_mom.sort_values(["trade_type", "date"])

# calcular MoM
df_mom["MoM"] = df_mom.groupby("trade_type")["Value"].pct_change()

# remover primeiro mês (NaN)
df_mom = df_mom.dropna(subset=["MoM"])

# transformar em porcentagem real (mais legível)
df_mom["MoM_pct"] = df_mom["MoM"] * 100

# gráfico separado (mais limpo)
chart = alt.Chart(df_mom).mark_bar(size=25).encode(
    x=alt.X("yearmonth(date):O", title="Month"),
    y=alt.Y("MoM_pct:Q", title="Change (%)"),
    
    # cor automática (melhor que manual)
    color=alt.condition(
        alt.datum.MoM_pct >= 0,
        alt.value("#00C853"),  # verde bonito
        alt.value("#D50000")   # vermelho forte
    ),

    column=alt.Column(
        "trade_type:N",
        title=None,
        spacing=40
    ),

    tooltip=[
        alt.Tooltip("yearmonth(date):T", title="Month"),
        alt.Tooltip("trade_type:N", title="Type"),
        alt.Tooltip("Value:Q", format=",.0f"),
        alt.Tooltip("MoM_pct:Q", format=".2f", title="% Change")
    ]
).properties(
    height=350
)

st.altair_chart(chart, use_container_width=True)
