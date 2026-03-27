from fastapi import APIRouter,Depends
from app.core.security.auth import get_current_user_id
from pydantic import BaseModel
from app.core.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

router = APIRouter()

class SyncRequest(BaseModel):
    timezone: str = "UTC"

@router.post("/auth/sync")
async def sync_user(request: SyncRequest,user_id: str= Depends(get_current_user_id),db: AsyncSession=Depends(get_db)):
    await db.execute(text(
        """
        INSERT INTO core.users (northpost_user_id, timezone)
        VALUES (:user_id, :timezone)
        ON CONFLICT (northpost_user_id)
        DO UPDATE SET timezone = :timezone, updated_at = NOW()
        """),
        {"user_id": user_id, "timezone": request.timezone}
    )
    await db.commit()
    
    return {"synced": True,"user_id":user_id,"timezone":request.timezone}