import joblib
import numpy as np
from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():
    bundle = joblib.load("ml/models/credit_model.pkl")

    if isinstance(bundle, dict):
        return (
            bundle["model"],
            bundle.get("explainer"),
            bundle.get("feature_names"),
            bundle.get("version", "v1")
        )

    # fallback (older model)
    return bundle, None, None, "v1"


def predict(features):
    model, explainer, feature_names, version = load_model()

    X = np.array([features])

    # probability of default
    prob = model.predict_proba(X)[0][1]

    # convert to score
    score = int(300 + (1 - prob) * 600)

    # tier mapping
    if score >= 750:
        tier = "excellent"
    elif score >= 650:
        tier = "good"
    elif score >= 550:
        tier = "fair"
    else:
        tier = "poor"

    # SHAP (if available)
    shap_values = []
    if explainer:
        shap_values = explainer(X).values[0]

    return score, tier, prob, shap_values, version