# ETL Pipeline Design Documentation

## 1. Database Schema Design

### 1.1 Design Philosophy

The database schema follows a **separation-of-concerns** principle:

- Raw client loan data is stored in a normalized table (`clients`)
- Derived, model-ready features are stored separately (`client_loan_features`)

### 1.2 Clients Table (Raw Data Layer)

The `clients` table stores validated, immutable loan-level records.

**Primary Key**
- `(client_id, loan_date)`
  - Allows multiple loans per client
  - Preserves temporal ordering of borrowing behavior

**Key Constraints & Assumptions**
- Age ≥ 18
- Credit score ∈ [300, 850]
- Loan amount > 0
- Loan term > 0

These constraints enforce **domain realism**, preventing invalid financial records.

**Indexes**
- `defaulted`: speeds up outcome-based analysis
- `credit_score`: supports creditworthiness queries
- `loan_date`: enables temporal analysis


### 1.3 Client Loan Features Table (Feature Store)

The `client_loan_features` table stores engineered variables used for modeling.
This table is derived entirely from `clients`.


## 2. Transformation Logic

Each engineered feature is motivated by credit risk theory (based on research):

| Feature | Description | Rationale |
|------|------|------|
| credit_utilization | loan_amount / account_balance | Higher utilization increases default risk |
| income_to_loan_ratio | annual_income / loan_amount | Measures repayment capacity |
| deposit_to_income_ratio | monthly_deposit / annual_income | Captures liquidity behavior |
| employment_tenure_years | months_at_company / 12 | Employment stability proxy |
| credit_score_bucket | Discretized credit score | Improves model interpretability |


All transformations are implemented in `src/etl/transform.py`.
