from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.db.session import Base

class UserProfile(Base):
    """Profile data mirroring Supabase Auth's user metadata."""
    __tablename__ = "profiles"
    id = Column(UUID(as_uuid=True), primary_key=True)  # Matches supabase.auth.users.id
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    applications = relationship("Application", back_populates="user")

class Application(Base):
    """Raw alternative data provided by the user for scoring."""
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    
    # Alternative Data Signals
    monthly_upi_txn_count = Column(Integer)
    avg_monthly_inflow = Column(Numeric(12, 2))
    utility_payment_streak = Column(Integer)
    mobile_recharge_freq = Column(Integer)
    gst_filed = Column(Boolean)
    rental_payment_months = Column(Integer)
    employment_type = Column(Text)
    years_at_address = Column(Numeric(4, 1))
    
    extra_data = Column(JSONB)  # Flexible field for future signals
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserProfile", back_populates="applications")
    score = relationship("Score", back_populates="application", uselist=False)

class Score(Base):
    """The generated result from the ML model."""
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), unique=True)
    
    score = Column(Integer, nullable=False)        # 300â€“900 range
    tier = Column(Text, nullable=False)           # poor|fair|good|excellent
    probability = Column(Numeric(5, 4), nullable=False)
    shap_values = Column(JSONB, nullable=False)   # Explainability (Top 5 factors)
    model_version = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="score")
