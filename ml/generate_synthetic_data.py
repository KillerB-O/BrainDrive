import numpy as np
import pandas as pd

# NOTE:
# This script is ONLY for generating synthetic training data.
# Not used in API / backend runtime.

print("Starting data generation...")

np.random.seed(42)
N = 5000

df = pd.DataFrame({
    "monthly_upi_txn_count": np.random.randint(1, 100, N),
    "avg_monthly_inflow": np.random.randint(5000, 50000, N),
    "utility_payment_streak": np.random.randint(0, 24, N),
    "mobile_recharge_freq": np.random.randint(0, 5, N),
    "gst_filed": np.random.randint(0, 2, N),
    "rental_payment_months": np.random.randint(0, 24, N),
    "years_at_address": np.random.uniform(0, 10, N),
    "employment_type": np.random.choice(
        ["salaried", "gig", "self_employed", "none"], N
    )
})

df["TARGET"] = (
    (df["avg_monthly_inflow"] < 15000) &
    (df["utility_payment_streak"] < 6)
).astype(int)

df.to_csv("data/application_train.csv", index=False)

print("✅ Synthetic data created successfully!")