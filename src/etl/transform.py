import pandas as pd

def transform_clients(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate client loan records.
    """
    df = df.copy()

    # Convert dates
    df["loan_date"] = pd.to_datetime(
        df["loan_date"],
        format="%d/%m/%Y",
        dayfirst=True
    ).dt.date


    # Remove duplicates (same client, same loan)
    df = df.drop_duplicates(subset=["client_id", "loan_date"])

    # Drop rows with critical missing values
    required_cols = [
        "client_id", "loan_date", "age", "employment_status",
        "annual_income", "credit_score", "loan_amount",
        "loan_term_months", "defaulted", "is_repeat_borrower"
    ]
    df = df.dropna(subset=required_cols)

    # Type casting
    df["client_id"] = df["client_id"].astype(int)
    df["age"] = df["age"].astype(int)
    df["months_at_company"] = df["months_at_company"].fillna(0).astype(int)
    df["credit_score"] = df["credit_score"].astype(int)
    df["loan_term_months"] = df["loan_term_months"].astype(int)

    df["annual_income"] = df["annual_income"].astype(float)
    df["loan_amount"] = df["loan_amount"].astype(float)
    df["account_balance"] = df["account_balance"].astype(float)
    df["monthly_deposit"] = df["monthly_deposit"].astype(float)

    df["defaulted"] = df["defaulted"].astype(bool)
    df["is_repeat_borrower"] = df["is_repeat_borrower"].astype(bool)

    # Business rules
    df = df[df["age"] >= 18]
    df = df[df["credit_score"].between(300, 850)]
    df = df[df["loan_amount"] > 0]
    df = df[df["loan_term_months"] > 0]
    df = df[df["annual_income"] >= 0]    
    
    # Credit score buckets
    df["credit_score_bucket"] = pd.cut(
        df["credit_score"],
        bins=[300, 580, 670, 740, 800, 850],
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

    # Feature engineering
    df["credit_utilization"] = df["loan_amount"] / (df["account_balance"] + 1)
    df["income_to_loan_ratio"] = df["annual_income"] / df["loan_amount"]
    df["deposit_to_income_ratio"] = df["monthly_deposit"] / (df["annual_income"] + 1)
    df["employment_tenure_years"] = df["months_at_company"] / 12
    df["credit_score_bucket"] = df["credit_score"] // 50
    df["is_repeat_borrower"] = df["is_repeat_borrower"]

    return df
