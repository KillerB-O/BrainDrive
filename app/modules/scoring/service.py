from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime
import json

from app.core.auth import get_current_user_id
from app.core.api.schemas import ApplicationInput

class ScoringService:
    """
    Handles credit scoring applications and history.
    Uses raw SQL to manage DB interactions via the shared context user_id.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_score(self, data: ApplicationInput):
        user_id = get_current_user_id()
        
        insert_query = text("""
            INSERT INTO applications (
                user_id, monthly_upi_txn_count, avg_monthly_inflow, 
                utility_payment_streak, mobile_recharge_freq, gst_filed, 
                rental_payment_months, employment_type, years_at_address, 
                extra_data, created_at
            ) VALUES (
                :uid, :upi, :inf, :strk, :rech, :gst, :rent, :emp, :yrs, :extra, :now
            ) RETURNING id
        """)
        
        result = await self.db.execute(insert_query, {
            "uid": user_id,
            "upi": data.monthly_upi_txn_count,
            "inf": data.avg_monthly_inflow,
            "strk": data.utility_payment_streak,
            "rech": data.mobile_recharge_freq,
            "gst": data.gst_filed,
            "rent": data.rental_payment_months,
            "emp": data.employment_type,
            "yrs": data.years_at_address,
            "extra": json.dumps(data.extra_data) if data.extra_data else None,
            "now": datetime.now()
        })
        app_id = result.scalar()
        
        # TODO: Add logic for ML-driven score calculation here.
        
        await self.db.commit()
        return {"application_id": app_id, "status": "processed"}

    async def get_history(self):
        user_id = get_current_user_id()
        
        query = text("""
            SELECT s.* FROM scores s
            JOIN applications a ON s.application_id = a.id
            WHERE a.user_id = :uid
            ORDER BY s.created_at DESC
        """)
        
        result = await self.db.execute(query, {"uid": user_id})
        return [dict(row._mapping) for row in result]
