import pandas as pd

def download_data():
    print("Streaming dataset...")

    url = "https://huggingface.co/datasets/WilgnerCH/canada-trade-data/resolve/main/canada_trade_full.csv.gz"

    chunks = pd.read_csv(
        url,
        usecols=["date", "Country", "trade_type", "Value"],
        dtype={"Country": "string", "trade_type": "string"},
        chunksize=100_000  # lê em partes
    )

    df_list = []

    for chunk in chunks:
        chunk = chunk[chunk["Country"] == "BR"]
        df_list.append(chunk)

    df = pd.concat(df_list)

    print("Final rows:", len(df))

    return df
