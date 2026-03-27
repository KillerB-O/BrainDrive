from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Any, Dict,List, Literal, Optional
from datetime import datetime


class ApplicationInput(BaseModel):
    """The shape of the data received from the user."""
    monthly_upi_txn_count: int = Field(ge=0, le=1000, description="Monthly UPI transactions count")
    avg_monthly_inflow: float = Field(ge=0, description="Average monthly credits")
    utility_payment_streak: int = Field(ge=0, le=12, description="Months of consecutive utility bills paid")
    mobile_recharge_freq: int = Field(ge=0, description="Number of mobile recharges per month")
    gst_filed: bool = Field(default=False, description="Has user filed GST in last 6 months?")
    rental_payment_months: int = Field(ge=0, description="History of rental payments in months")
    employment_type: Literal["salaried", "gig", "self_employed", "none"]
    years_at_address: float = Field(ge=0, description="Years lived at current address")
    extra_data: Optional[Dict[str, Any]] = None

class Factor(BaseModel):
    feature: str
    impact: float
    direction: Literal["positive", "negative"]

class ScoreResponse(BaseModel):
    """How we return the credit score result to the user."""
    id: str
    application_id: int
    score: int
    tier: str
    probability: float
    model_version: str
    summary: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
