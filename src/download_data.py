import pandas as pd

def download_data():
    print("Streaming and aggregating dataset...")

    url = "https://huggingface.co/datasets/WilgnerCH/canada-trade-data/resolve/main/canada_trade_full.csv.gz"

    chunks = pd.read_csv(
        url,
        usecols=["date", "Country", "trade_type", "Value"],
        dtype={"Country": "string", "trade_type": "string"},
        chunksize=100_000  # lê em partes
    )

    agg_list = []

    for chunk in chunks:
        # Filtrar Brasil
        chunk = chunk[chunk["Country"] == "BR"]

        # Converter valor
        chunk["Value"] = pd.to_numeric(chunk["Value"], errors="coerce")
        chunk = chunk.dropna(subset=["Value"])

        # Converter data
        chunk["date"] = pd.to_datetime(chunk["date"], errors="coerce")
        chunk = chunk.dropna(subset=["date"])

        # Agrupar por mês
        chunk["year_month"] = chunk["date"].dt.to_period("M")

        agg = (
            chunk.groupby(["year_month", "trade_type"])["Value"]
            .sum()
        )

        agg_list.append(agg)

    # juntar tudo e reagrupar
    df = (
        pd.concat(agg_list)
        .groupby(level=[0, 1])
        .sum()
        .reset_index()
    )

    # Padronizar nome
    df = df.rename(columns={"year_month": "date"})

    print("Final aggregated rows:", len(df))

    return df
