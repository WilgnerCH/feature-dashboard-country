import pandas as pd

def process_data(df):
    print("Final processing...")

    # Converter date
    df["date"] = df["date"].astype(str)
    df["date"] = pd.to_datetime(df["date"])

    return df
