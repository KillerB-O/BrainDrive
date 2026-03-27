from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db
from app.core.auth import get_current_user

from app.modules.scoring.schema import ApplicationInput, ScoreResponse
from app.modules.scoring.service import create_application, get_user_scores, get_score_by_id

router = APIRouter()

@router.post("/apply")
async def apply(
    data: ApplicationInput,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await create_application(data, user["id"], db)


@router.get("/my-scores", response_model=List[ScoreResponse])
async def my_scores(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await get_user_scores(user["id"], db)


@router.get("/scores/{score_id}", response_model=ScoreResponse)
async def get_score(
    score_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    score = await get_score_by_id(score_id, user["id"], db)
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score
