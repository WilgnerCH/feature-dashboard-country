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
# MoM (ADVANCED BAR CHART)
# ======================
st.subheader("📊 Month-over-Month Change (Import vs Export)")

df_mom = df.copy()

# ordenar corretamente
df_mom = df_mom.sort_values(["trade_type", "date"])

# calcular MoM por tipo
df_mom["MoM"] = df_mom.groupby("trade_type")["Value"].pct_change()

# cor condicional
df_mom["color"] = df_mom["MoM"].apply(
    lambda x: "green" if x >= 0 else "red"
)

# gráfico Altair
chart = alt.Chart(df_mom).mark_bar().encode(
    x=alt.X("date:T", title="Date"),
    y=alt.Y("MoM:Q", title="MoM Change (%)"),
    color=alt.Color("color:N", scale=None),
    column=alt.Column("trade_type:N", title=None),
    tooltip=[
        alt.Tooltip("date:T", title="Date"),
        alt.Tooltip("trade_type:N", title="Type"),
        alt.Tooltip("Value:Q", title="Value", format=",.0f"),
        alt.Tooltip("MoM:Q", title="MoM", format=".2%")
    ]
).properties(
    height=350
)

st.altair_chart(chart, use_container_width=True)
