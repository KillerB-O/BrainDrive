import pandas as pd
import xgboost as xgb
import shap
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from features import create_features, FEATURE_NAMES

print("🚀 Starting training with Kaggle data...")

df = pd.read_csv("data/application_train.csv")

print("✅ Data loaded")


def map_kaggle(df):
    df = df.copy()

    df["avg_monthly_inflow"] = df["AMT_INCOME_TOTAL"]
    df["years_at_address"] = np.abs(df["DAYS_EMPLOYED"]) / 365

    df["monthly_upi_txn_count"] = (df["avg_monthly_inflow"] / 2000).clip(1, 100)

    df["utility_payment_streak"] = (
        np.abs(df["DAYS_EMPLOYED"]) / 100
    ).clip(0, 24)

    df["mobile_recharge_freq"] = np.random.randint(1, 5, len(df))
    df["gst_filed"] = (df["avg_monthly_inflow"] > 30000).astype(int)
    df["rental_payment_months"] = (df["years_at_address"] * 2).clip(0, 24)

    df["employment_type"] = np.where(
        df["avg_monthly_inflow"] > 30000,
        "salaried",
        "gig"
    )

    # =========================
# STRONG KAGGLE FEATURES
# =========================

    df["income_credit_ratio"] = df["AMT_INCOME_TOTAL"] / (df["AMT_CREDIT"] + 1)
    df["annuity_income_ratio"] = df["AMT_ANNUITY"] / (df["AMT_INCOME_TOTAL"] + 1)   
    df["employment_years"] = abs(df["DAYS_EMPLOYED"]) / 365
    df["age_years"] = abs(df["DAYS_BIRTH"]) / 365
    df["credit_goods_ratio"] = df["AMT_CREDIT"] / (df["AMT_GOODS_PRICE"] + 1)

# EXT_SOURCE (VERY IMPORTANT)
    df["ext_mean"] = df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].mean(axis=1)

    return df

# Apply mapping
df = map_kaggle(df)

# Feature engineering
df = create_features(df)

# Drop rows without target
df = df.dropna(subset=["TARGET"])

MODEL_FEATURES = FEATURE_NAMES +  [
    "income_credit_ratio",
    "annuity_income_ratio",
    "employment_years",
    "age_years",
    "credit_goods_ratio",
    "ext_mean"
]

X = df[MODEL_FEATURES]
y = df["TARGET"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Handle imbalance
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

model = xgb.XGBClassifier(
    n_estimators=800,
    max_depth=6,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="auc",
    scale_pos_weight=scale_pos_weight,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
preds = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, preds)

print(f"🎯 AUC: {auc:.4f}")

# SHAP
explainer = shap.TreeExplainer(model)

# Save model
joblib.dump({
    "model": model,
    "explainer": explainer,
    "feature_names": MODEL_FEATURES,
    "auc": auc,
    "version": "v2_kaggle"
}, "ml/models/credit_model.pkl")

print("💾 Model saved (Kaggle-trained) ✅")

import matplotlib.pyplot as plt 
from sklearn.metrics import roc_curve

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, preds)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
plt.plot([0, 1], [0, 1], linestyle='--')  # random baseline

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.show()