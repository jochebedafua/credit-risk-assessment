from src.etl.extract import extract_clients
from src.etl.transform import transform_clients
from src.etl.load import load_clients, load_features

RAW_PATH = "data/client_loan_data.csv"

def run():
    df = extract_clients(RAW_PATH)
    df_transformed = transform_clients(df)

    load_clients(df)
    load_features(df_transformed)

if __name__ == "__main__":
    run()

