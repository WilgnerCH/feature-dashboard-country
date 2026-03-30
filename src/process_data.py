import pandas as pd


def process_data(df):

    print("Processing data...")

    # garantir tipos
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # remover valores inválidos
    df = df.dropna(subset=["Value", "Country", "trade_type"])

    # 🔥 AGREGAÇÃO POR PAÍS + IMPORT/EXPORT
    df_country = (
        df.groupby(["date", "Country", "trade_type"])["Value"]
        .sum()
        .reset_index()
    )

    print("Processed dataset size:", len(df_country))

    return df_country
