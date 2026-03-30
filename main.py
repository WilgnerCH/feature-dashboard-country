from src.download_data import download_data
from src.process_data import process_data


def main():

    print("Starting pipeline...")

    df = download_data()

    df_brazil = process_data(df)

    # salvar arquivo leve
    df_brazil.to_csv("brazil_trade_summary.csv", index=False)

    print("Dataset created: brazil_trade_summary.csv")


if __name__ == "__main__":
    main()
