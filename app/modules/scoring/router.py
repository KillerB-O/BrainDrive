from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.auth import authenticate_user
from app.modules.scoring.schemas import ApplicationInput
from app.modules.scoring.service import ScoringService

router = APIRouter()

@router.post("/apply", status_code=status.HTTP_201_CREATED)
async def submit_application(
    application: ApplicationInput,
    _ = Depends(authenticate_user), # Injects user_id into context
    db: AsyncSession = Depends(get_db)
):
    """
    Submits application data. 
    user_id is handled automatically via ContextVar.
    """
    service = ScoringService(db)
    return await service.process_score(application)

@router.get("/my-scores")
async def get_user_scores(
    _ = Depends(authenticate_user), # Ensures context is set
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves history for the authenticated user.
    """
    service = ScoringService(db)
    return await service.get_history()
