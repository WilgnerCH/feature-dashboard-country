import pandas as pd

def process_data(df):
    print("Processing Brazil trade data...")

    # Garantir numérico
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # Remover inválidos
    df = df.dropna(subset=["Value", "Country", "trade_type"])

    # Filtrar Brasil
    df = df[df["Country"] == "BR"]

    # Converter data
    df["date"] = pd.to_datetime(df["date"])

    # Agregação
    df_brazil = (
        df.groupby(["date", "trade_type"])["Value"]
        .sum()
        .reset_index()
    )

    print("Brazil dataset size:", len(df_brazil))

    return df_brazil
