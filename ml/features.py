import numpy as np

# =========================
# MODEL FEATURE CONTRACT
# =========================
FEATURE_NAMES = [
    "monthly_upi_txn_count",
    "avg_monthly_inflow",
    "log_monthly_inflow",
    "utility_payment_streak",
    "mobile_recharge_freq",
    "gst_filed",
    "rental_payment_months",
    "years_at_address",
    "employment_salaried",
    "employment_gig",
    "employment_self_employed",
    "inflow_per_txn",
    "payment_reliability",
    "income_stability",
    "txn_intensity",
    "activity_score",
    "risk_flag",
]

# =========================
# KAGGLE → MODEL MAPPING
# =========================
def map_kaggle_to_model(df):
    df = df.copy()

    # Base mapping FIRST
    df["avg_monthly_inflow"] = df["AMT_INCOME_TOTAL"]

    # Derived base fields
    df["years_at_address"] = np.abs(df["DAYS_EMPLOYED"]) / 365

    # Now safe to use
    df["monthly_upi_txn_count"] = (df["avg_monthly_inflow"] / 2000).clip(1, 100)

    df["utility_payment_streak"] = (
        np.abs(df["DAYS_EMPLOYED"]) / 100
    ).clip(0, 24)

    df["mobile_recharge_freq"] = np.random.randint(1, 5, len(df))

    df["gst_filed"] = (df["avg_monthly_inflow"] > 30000).astype(int)

    df["rental_payment_months"] = (df["years_at_address"] * 2).clip(0, 24)

    df["employment_type"] = np.where(
    df["DAYS_EMPLOYED"] < -2000,
    "salaried",
    np.where(df["DAYS_EMPLOYED"] < -500, "self_employed", "gig")
)

    return df

# =========================
# FEATURE ENGINEERING
# =========================
def create_features(df):
    df = df.copy()
    df = df.fillna(0)

    df["log_monthly_inflow"] = np.log1p(df["avg_monthly_inflow"])

    df["inflow_per_txn"] = df["avg_monthly_inflow"] / df["monthly_upi_txn_count"].clip(lower=1)

    df["payment_reliability"] = (
        df["utility_payment_streak"] + df["rental_payment_months"]
    ) / 2

    df["employment_salaried"] = (df["employment_type"] == "salaried").astype(int)
    df["employment_gig"] = (df["employment_type"] == "gig").astype(int)
    df["employment_self_employed"] = (df["employment_type"] == "self_employed").astype(int)

    # =========================
# NEW STRONG FEATURES
# =========================

# Income stability proxy
    df["income_stability"] = df["avg_monthly_inflow"] / (df["years_at_address"] + 1)

# Transaction intensity
    df["txn_intensity"] = df["monthly_upi_txn_count"] * df["mobile_recharge_freq"]

# Financial activity score
    df["activity_score"] = (
    df["monthly_upi_txn_count"] +
    df["mobile_recharge_freq"] +
    df["utility_payment_streak"]
    )

# Risk proxy (low income + low stability)
    df["risk_flag"] = (
    (df["avg_monthly_inflow"] < 15000) &
    (df["utility_payment_streak"] < 5)
    ).astype(int)
    return df

