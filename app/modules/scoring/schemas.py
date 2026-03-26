from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from uuid import UUID
from datetime import datetime

class ApplicationInput(BaseModel):
    monthly_upi_txn_count: int = Field(ge=0, le=1000)
    avg_monthly_inflow: float = Field(ge=0)
    utility_payment_streak: int = Field(ge=0, le=12)
    mobile_recharge_freq: int = Field(ge=0)
    gst_filed: bool = False
    rental_payment_months: int = Field(ge=0)
    employment_type: Literal["salaried", "gig", "self_employed", "none"]
    years_at_address: float = Field(ge=0)
    extra_data: Optional[Dict[str, Any]] = None

class Factor(BaseModel):
    feature: str
    impact: float
    direction: Literal["positive", "negative"]

class ScoreResponse(BaseModel):
    application_id: int
    score: int
    tier: str
    probability: float
    top_factors: List[Factor]
    created_at: datetime

    class Config:
        from_attributes = True
