from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.db.session import get_db
from app.core.api.schemas import ApplicationInput, ScoreResponse, ExplanationRequest, ExplanationResponse
from app.core.auth import get_current_user_id

router = APIRouter()

@router.post("/scores", response_model=ScoreResponse, status_code=status.HTTP_201_CREATED)
async def create_score(
    application: ApplicationInput,
    user_id: UUID = Depends(get_current_user_id), # <-- Securely get the user UUID
    db: AsyncSession = Depends(get_db)
):
    # TODO: Implement feature engineering, scoring, and saving to DB using the user_id
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/scores/{application_id}", response_model=ScoreResponse)
async def get_score(
    application_id: int,
    db: AsyncSession = Depends(get_db)
):
    # TODO: Implement retrieval from DB
    raise HTTPException(status_code=501, detail="Not implemented")

@router.post("/scores/{score_id}/explain", response_model=ExplanationResponse)
async def explain_score(
    score_id: int,
    request: ExplanationRequest,
    db: AsyncSession = Depends(get_db)
):
    # TODO: Implement LLM explanation logic
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/health")
async def health_check():
    return {"status": "ok"}
