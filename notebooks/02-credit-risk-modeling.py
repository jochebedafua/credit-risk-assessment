# ---
# jupyter:
#   jupytext:
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
# # Machine Learning Model Design

# %% [markdown]
# ## 1. Setup & Imports

# %%
import sys
from pathlib import Path

# Set the project root
project_root = Path().resolve().parent  # if notebook is in a subfolder like 'notebooks'
sys.path.append(str(project_root))

# print(sys.path)

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine
from src.db.connection import get_engine

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    GridSearchCV
)

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    roc_auc_score,
    classification_report,
    confusion_matrix,
    RocCurveDisplay
)

import joblib
import warnings
warnings.filterwarnings("ignore")

RANDOM_STATE = 42

# %% [markdown]
# ## 2. Load Data

# %%
# load data
engine = get_engine()

df = pd.read_sql(
    "SELECT * FROM client_loan_features",
    engine
)
df.head()

# %%
df.shape

# %% [markdown]
# ## 3. Target & Feature Separation

# %%
# Define Features and Target

X = df.drop(columns=["client_id", "loan_date", "defaulted"])
y = df["defaulted"]

# %% [markdown]
# ## 4. Train–Validation–Test Split

# %%
# First split: train+val vs test
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=RANDOM_STATE
)

# %%
# Second split: train vs validation
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp,
    test_size=0.25,   # 0.25 * 0.8 = 0.2
    stratify=y_temp,
    random_state=RANDOM_STATE
)

# %% [markdown]
# ## 5. Feature Preprocessing

# %%
# Identify feature types

numeric_features = X.columns.tolist()
numeric_features

# %%
# Preprocessing pipeline

from sklearn.impute import SimpleImputer

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features)
    ]
)

# %% [markdown]
# ## 6. Baseline Model

# %%
X_train.isna().mean().sort_values(ascending=False)

# %%
#logistic regression

baseline_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=RANDOM_STATE
    ))
])

baseline_pipeline.fit(X_train, y_train)


# %%
val_pred_proba = baseline_pipeline.predict_proba(X_val)[:, 1]
roc_auc_score(y_val, val_pred_proba)

# %% [markdown]
# ## 7. Model Selection

# %%
models = {
    "logistic": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=RANDOM_STATE
    ),
    "random_forest": RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=RANDOM_STATE
    ),
    "gradient_boosting": GradientBoostingClassifier(
        random_state=RANDOM_STATE
    )
}

# %%
# Train and compare
results = []

for name, model in models.items():
    pipe = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    
    pipe.fit(X_train, y_train)
    val_proba = pipe.predict_proba(X_val)[:, 1]
    
    results.append({
        "model": name,
        "roc_auc": roc_auc_score(y_val, val_proba)
    })

pd.DataFrame(results).sort_values("roc_auc", ascending=False)


# %% [markdown]
# ## 8. Hyperparameter Tuning

# %%
gb_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", GradientBoostingClassifier(
        random_state=RANDOM_STATE
    ))
])

param_grid = {
    "model__n_estimators": [100, 200, 300],
    "model__learning_rate": [0.01, 0.05, 0.1],
    "model__max_depth": [2, 3, 4],
    "model__min_samples_leaf": [50, 100],
    "model__subsample": [0.8, 1.0]
}


# %%
# Cross-validation setup

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=RANDOM_STATE
)

# %%
# Grid search

gb_grid = GridSearchCV(
    gb_pipeline,
    param_grid=param_grid,
    scoring="roc_auc",
    cv=cv,
    n_jobs=-1,
    verbose=2
)

gb_grid.fit(X_train, y_train)


# %%
best_gb_model = gb_grid.best_estimator_
gb_grid.best_params_

# %% [markdown]
# ## 9. Model Evaluation

# %%
val_proba = best_gb_model.predict_proba(X_val)[:, 1]

val_auc = roc_auc_score(y_val, val_proba)
val_auc

# %%
RocCurveDisplay.from_predictions(y_val, val_proba)
plt.title("Gradient Boosting – Validation ROC Curve")
plt.show()

# %% [markdown]
# ## 10. Model Interpretation

# %%
importances = best_gb_model.named_steps["model"].feature_importances_

feature_importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": importances
}).sort_values("importance", ascending=False)

feature_importance_df

# %%
plt.figure(figsize=(8, 5))
sns.barplot(
    data=feature_importance_df.head(10),
    x="importance",
    y="feature"
)
plt.title("Top Feature Importances – Gradient Boosting")
plt.show()

# %% [markdown]
# ## 11. Model Selection & Test Set Evaluation

# %%
# Test ROC-AUC

test_proba = best_gb_model.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, test_proba)
test_auc

# %%
# Test ROC Curve

RocCurveDisplay.from_predictions(y_test, test_proba)
plt.title("Gradient Boosting – Test ROC Curve")
plt.show()

# %%
test_preds = (test_proba >= 0.4).astype(int)

print(classification_report(y_test, test_preds))

# %% [markdown]
# ## Summary

# %% [markdown]
# A Gradient Boosting classifier was selected as the final model after hyperparameter tuning using stratified cross-validation. 
#
# The model achieved the highest ROC-AUC on the validation set and demonstrated strong generalization performance on the test set. 
#
# Gradient Boosting effectively captures non-linear relationships and feature interactions in borrower behavior data.
