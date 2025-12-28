# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Exploratory Data Analysis
#
# This notebook explores the engineered dataset to understand distributions, patterns, correlations, and relationships that may influence loan default.
#
# The insights here will guide feature selection and modeling.

# %% [markdown]
# ## 1. Setup & Imports

# %%
import sys
from pathlib import Path

# Set the project root (adjust if your notebook is not in the root)
project_root = Path().resolve().parent  # if notebook is in a subfolder like 'notebooks'
sys.path.append(str(project_root))

# print(sys.path)


# %%
# Import libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.db.connection import get_engine

plt.style.use("default")

# %%
# Load data

engine = get_engine()
df = pd.read_sql("SELECT * FROM client_loan_features", engine)
df.head()

# %% [markdown]
# ## 2. Exploratory Data Analysis

# %%
# Basic info
df.info()

# %%
# Missing values
df.isna().sum()

# %%
# Summary statistics
df.describe(include='all').T

# %%
df["defaulted"].value_counts(normalize=True)

# %%
sns.countplot(x="defaulted", data=df)
plt.title("Loan Default Distribution")
plt.xlabel("Defaulted")
plt.ylabel("Count")
plt.show()


# %%
# Distribution of numerical features
numerical_cols = [
    "credit_utilization",
    "income_to_loan_ratio",
    "deposit_to_income_ratio",
    "employment_tenure_years"
]

df[numerical_cols].hist(bins=30, figsize=(12,8))
plt.suptitle("Distribution of Engineered Features")
plt.show()


# %%
# boxplots to find outliers
for col in numerical_cols:
    plt.figure(figsize=(6,2))
    sns.boxplot(x=df[col])
    plt.title(col)
    plt.show()

# %%
# Correlations
corr = df.drop(columns=["client_id", "loan_date"]).corr()

plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Feature Correlations")
plt.show()


# %%
corr["defaulted"].sort_values(ascending=False)

# %%
# Default vs Non-Default Comparisons

sns.boxplot(x="defaulted", y="credit_utilization", data=df)
plt.title("Credit Utilization vs Default Status")
plt.show()

# %%
sns.boxplot(x="defaulted", y="income_to_loan_ratio", data=df)
plt.title("Income-to-Loan Ratio vs Default Status")
plt.show()

# %%
sns.boxplot(x="defaulted", y="employment_tenure_years", data=df)
plt.title("Employment Tenure vs Default Status")
plt.show()

# %%
sns.countplot(
    x="credit_score_bucket",
    hue="defaulted",
    data=df
)
plt.title("Credit Score Buckets vs Default")
plt.show()


# %%
sns.countplot(
    x="is_repeat_borrower",
    hue="defaulted",
    data=df
)
plt.title("Repeat Borrower Status vs Default")
plt.show()

# %%
