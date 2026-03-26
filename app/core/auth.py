from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from uuid import UUID
from typing import Optional
from contextvars import ContextVar
from app.core.config import get_settings

security = HTTPBearer()
settings = get_settings()

user_id_ctx: ContextVar[Optional[UUID]] = ContextVar("user_id", default=None)

async def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    """
    Decodes Supabase JWT and injects the user's UUID into the request-local context.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, 
            settings.supabase_jwt_secret, 
            algorithms=["HS256"], 
            options={"verify_aud": False}
        )
        user_id = UUID(payload.get("sub"))
        user_id_ctx.set(user_id)
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )

def get_current_user_id() -> UUID:
    """
    Retrieves the injected user_id from the context. 
    Must be called within an authenticated request.
    """
    uid = user_id_ctx.get()
    if not uid:
        raise RuntimeError("User context missing")
    return uid
