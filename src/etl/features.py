import pandas as pd

def build_loan_features(df: pd.DataFrame) -> pd.DataFrame:
    features = pd.DataFrame()

    features["client_id"] = df["client_id"]
    features["loan_date"] = df["loan_date"]

    features["credit_utilization"] = df["loan_amount"] / (
        df["account_balance"].replace(0, 1)
    )

    features["income_to_loan_ratio"] = df["annual_income"] / df["loan_amount"]
    features["deposit_to_income_ratio"] = (
        df["monthly_deposit"] * 12
    ) / df["annual_income"]

    features["employment_tenure_years"] = df["months_at_company"] / 12
    features["credit_score_bucket"] = df["credit_score"] // 50

    features["is_repeat_borrower"] = df["is_repeat_borrower"]
    features["defaulted"] = df["defaulted"]

    return features
