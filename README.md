# Credit Risk Assessment

## Overview
This project analyzes borrower data to understand why clients are not repaying their loans and how to make better lending decisions.

## Project Structure
- `notebooks/` – Exploratory and modeling notebooks
- `src/` – Reusable data processing and modeling code
- `data/` – Raw data
- `docs/` – Schema design and transformation logic
- `schema/` – Database setup for data and engineered features

## Run the Project
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# install/start (macOS)
brew install postgresql
brew services start postgresql

# create DB and user
psql postgres
CREATE DATABASE credit_risk;
CREATE USER credit_user;
GRANT ALL PRIVILEGES ON DATABASE credit_risk TO credit_user;
\q

# set env (or .env)
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=credit_risk
export DB_USER=credit_user

# Run ETL (uses src/etl/run_etl.py)
python -m src.etl.run_etl

# EDA & Modeling: Start Jupyter and run the notebooks:
jupyter lab
```