import pandas as pd


def process_data(df):

    print("Processing Brazil trade data...")

    # garantir numérico
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # remover inválidos
    df = df.dropna(subset=["Value", "Country", "trade_type"])

    # 🇧🇷 FILTRO BRASIL
    df = df[df["Country"] == "BR"]

    # 🔥 AGREGAÇÃO (Import vs Export por data)
    df_brazil = (
        df.groupby(["date", "trade_type"])["Value"]
        .sum()
        .reset_index()
    )

    print("Brazil dataset size:", len(df_brazil))

    return df_brazil
