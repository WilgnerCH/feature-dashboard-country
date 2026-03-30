import altair as alt

st.subheader("📊 Month-over-Month Change (Imports)")

# pegar apenas import
df_import = df[df["trade_type"] == "Import"].copy()

# ordenar
df_import = df_import.sort_values("date")

# calcular variação MoM
df_import["MoM"] = df_import["Value"].pct_change()

# criar coluna de cor
df_import["color"] = df_import["MoM"].apply(
    lambda x: "green" if x >= 0 else "red"
)

# gráfico Altair
chart = alt.Chart(df_import).mark_bar().encode(
    x=alt.X("date:T", title="Date"),
    y=alt.Y("MoM:Q", title="MoM Change (%)"),
    color=alt.Color("color:N", scale=None),
    tooltip=["date", "Value", "MoM"]
).properties(
    height=400
)

st.altair_chart(chart, use_container_width=True)
