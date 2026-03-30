import pandas as pd


def download_data():

    print("Downloading data from Hugging Face...")

    url = "https://huggingface.co/datasets/WilgnerCH/canada-trade-data/resolve/main/canada_trade_full.csv.gz"

    df = pd.read_csv(url)

    print("Data loaded:", len(df))

    return df
