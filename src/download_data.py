import pandas as pd


def download_data():

    print("Downloading dataset...")

    url = "https://huggingface.co/datasets/WilgnerCH/canada-trade-data/resolve/main/canada_trade_full.csv.gz"

    # limitar leitura
    df = pd.read_csv(
        url,
        usecols=["date", "Country", "trade_type", "Value"],
        dtype={"Country": "string", "trade_type": "string"},
        low_memory=False
    )

    print("Rows loaded:", len(df))

    return df
