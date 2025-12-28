from sqlalchemy.dialects.postgresql import insert
from src.db.connection import get_engine

def load_clients(df):
    '''
    Docstring for load_clients
    
    :param df: Description
    '''
    engine = get_engine()
    df.to_sql("clients", engine, if_exists="append", index=False)


def load_features(df):
    '''
    Docstring for load_features
    
    :param df: Description
    '''
    engine = get_engine()
    features = df[[
        "client_id", "loan_date",
        "credit_utilization",
        "income_to_loan_ratio",
        "deposit_to_income_ratio",
        "employment_tenure_years",
        "credit_score_bucket",
        "is_repeat_borrower",
        "defaulted"
    ]]
    features.to_sql("client_loan_features", engine, if_exists="append", index=False)
