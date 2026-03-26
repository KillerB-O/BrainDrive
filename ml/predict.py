import pandas as pd
import joblib
import numpy as np

from ml.features import create_features, map_kaggle_to_model

# Load model
bundle = joblib.load("ml/models/credit_model.pkl")
model = bundle["model"]
FEATURES = bundle["feature_names"]

# Load input (test / UI data)
df = pd.read_csv("data/application_test.csv")

print("✅ Loaded data")

# Step 1 — Mapping
df = map_kaggle_to_model(df)

# Step 2 — Base feature engineering
df = create_features(df)

# =========================
# STEP 3 — STRONG FEATURES (MUST MATCH TRAINING)
# =========================

# EXT_SOURCE features
df["ext_mean"] = df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].mean(axis=1)
df["ext_max"] = df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].max(axis=1)

# Financial ratios
df["income_credit_ratio"] = df["AMT_INCOME_TOTAL"] / (df["AMT_CREDIT"] + 1)
df["annuity_income_ratio"] = df["AMT_ANNUITY"] / (df["AMT_INCOME_TOTAL"] + 1)

# Stability
df["employment_years"] = abs(df["DAYS_EMPLOYED"]) / 365
df["age_years"] = abs(df["DAYS_BIRTH"]) / 365

# Family-based signal
df["income_per_family"] = df["AMT_INCOME_TOTAL"] / (df["CNT_FAM_MEMBERS"] + 1)

print("✅ Strong features added")

# Step 4 — Select correct features (VERY IMPORTANT)
X = df[FEATURES]

# Step 5 — Predict
preds = model.predict_proba(X)[:, 1]

# Step 6 — Convert to score
scores = [int(300 + (1 - p) * 600) for p in preds]

print("🎯 Scores:", scores[:10])