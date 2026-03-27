from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.scoring.repository import insert_application, insert_score, fetch_scores, fetch_score_by_id
from app.modules.scoring.model import predict
from app.modules.scoring.schema import ApplicationInput

async def create_application(data: ApplicationInput, user_id: str, db: AsyncSession):
    # 1. Store application data
    app_id = await insert_application(db, data, user_id)
    
    # 2. Extract features for model
    # Note: Model expects a flat list of features
    features = [
        data.monthly_upi_txn_count,
        data.avg_monthly_inflow,
        data.utility_payment_streak,
        data.mobile_recharge_freq,
        1.0 if data.gst_filed else 0.0,
        data.rental_payment_months,
        data.years_at_address
    ]
    
    # 3. Predict using ML model
    score, tier, prob, shap_values, version = predict(features)
    
    # 4. Store score results
    await insert_score(db, app_id, score, tier, prob, shap_values, version)
    
    return {
        "application_id": app_id,
        "score": score,
        "tier": tier,
        "probability": prob,
        "model_version": version,
        "summary": f"Your alternative credit score is {score} ({tier.upper()})."
    }

async def get_user_scores(user_id: str, db: AsyncSession):
    return await fetch_scores(db, user_id)

async def get_score_by_id(score_id: int, user_id: str, db: AsyncSession):
    return await fetch_score_by_id(db, score_id, user_id)
