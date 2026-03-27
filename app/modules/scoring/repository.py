from sqlalchemy import text

async def insert_application(db, data, user_id):
    result = await db.execute(
        text("""
        INSERT INTO applications (
            user_id,
            monthly_upi_txn_count,
            avg_monthly_inflow,
            utility_payment_streak,
            mobile_recharge_freq,
            gst_filed,
            rental_payment_months,
            employment_type,
            years_at_address
        )
        VALUES (
            :user_id,
            :txn,
            :inflow,
            :utility,
            :recharge,
            :gst,
            :rental,
            :employment,
            :years
        )
        RETURNING id
        """),
        {
            "user_id": user_id,
            "txn": data.monthly_upi_txn_count,
            "inflow": data.avg_monthly_inflow,
            "utility": data.utility_payment_streak,
            "recharge": data.mobile_recharge_freq,
            "gst": data.gst_filed,
            "rental": data.rental_payment_months,
            "employment": data.employment_type,
            "years": data.years_at_address,
        }
    )
    return result.scalar()


async def insert_score(db, app_id, score, tier, prob, shap, version):
    # Ensure shap is a list for JSONB column
    shap_data = list(shap[:5]) if shap is not None and len(shap) > 0 else []
    
    await db.execute(
        text("""
        INSERT INTO scores (
            application_id,
            score,
            tier,
            probability,
            shap_values,
            model_version
        )
        VALUES (
            :app_id,
            :score,
            :tier,
            :prob,
            :shap,
            :version
        )
        """),
        {
            "app_id": app_id,
            "score": score,
            "tier": tier,
            "prob": prob,
            "shap": shap_data,
            "version": version
        }
    )
    await db.commit()


async def fetch_scores(db, user_id):
    result = await db.execute(
        text("""
        SELECT s.id, s.application_id, s.score, s.tier, s.probability, s.model_version, s.created_at
        FROM scores s
        JOIN applications a ON a.id = s.application_id
        WHERE a.user_id = :user_id
        ORDER BY s.created_at DESC
        """),
        {"user_id": user_id}
    )

    rows = result.fetchall()

    return [
        {
            "id": str(r.id),
            "application_id": r.application_id,
            "score": r.score,
            "tier": r.tier,
            "probability": float(r.probability),
            "model_version": r.model_version,
            "created_at": r.created_at,
            "summary": f"Alternative Credit Score: {r.score} ({r.tier.upper()})"
        }
        for r in rows
    ]


async def fetch_score_by_id(db, score_id, user_id):
    result = await db.execute(
        text("""
        SELECT s.id, s.application_id, s.score, s.tier, s.probability, s.model_version, s.created_at
        FROM scores s
        JOIN applications a ON a.id = s.application_id
        WHERE s.id = :score_id AND a.user_id = :user_id
        """),
        {"score_id": score_id, "user_id": user_id}
    )

    r = result.fetchone()
    if not r:
        return None

    return {
        "id": str(r.id),
        "application_id": r.application_id,
        "score": r.score,
        "tier": r.tier,
        "probability": float(r.probability),
        "model_version": r.model_version,
        "created_at": r.created_at,
        "summary": f"Alternative Credit Score: {r.score} ({r.tier.upper()})"
    }