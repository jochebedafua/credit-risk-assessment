-- Client loan table schema
CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 18),
    employment_status VARCHAR(50) NOT NULL,
    months_at_company INTEGER CHECK (months_at_company >= 0),
    annual_income NUMERIC NOT NULL CHECK (annual_income >= 0),
    credit_score INTEGER NOT NULL CHECK (credit_score BETWEEN 300 AND 850),
    account_balance NUMERIC,
    monthly_deposit NUMERIC CHECK (monthly_deposit >= 0),
    is_repeat_borrower BOOLEAN NOT NULL,
    loan_amount NUMERIC NOT NULL CHECK (loan_amount > 0),
    loan_term_months INTEGER NOT NULL CHECK (loan_term_months > 0),
    defaulted BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (client_id, loan_date)
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_clients_defaulted ON clients(defaulted);
CREATE INDEX IF NOT EXISTS idx_clients_credit_score ON clients(credit_score);
CREATE INDEX IF NOT EXISTS idx_clients_loan_date ON clients(loan_date);

-- Feature table schema
CREATE TABLE IF NOT EXISTS client_loan_features (
    client_id INTEGER,
    loan_date DATE,
    credit_utilization NUMERIC,
    income_to_loan_ratio NUMERIC,
    deposit_to_income_ratio NUMERIC,
    employment_tenure_years NUMERIC,
    credit_score_bucket INTEGER,
    is_repeat_borrower BOOLEAN,
    defaulted BOOLEAN,
    PRIMARY KEY (client_id, loan_date)
);
