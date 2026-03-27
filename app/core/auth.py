from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
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
    if not token or token == "undefined":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid token",
        )
        
    # Check if the JWT secret is available, as it's crucial for ES256
    if not settings.supabase_jwt_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT secret not configured. Cannot authenticate.",
        )

    try:
        # Using ES256 algorithm as specified.
        # IMPORTANT: For ES256, settings.supabase_jwt_secret MUST be an EC public key in PEM format.
        # If it's a string secret, ES256 will fail with errors like "Unable to load PEM file".
        payload = jwt.decode(
            token, 
            settings.supabase_jwt_secret, 
            algorithms=["ES256"], # Explicitly using ES256 as requested
            options={"verify_aud": False}
        )
        
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim",
            )
        
        user_id = UUID(user_id_str)
        user_id_ctx.set(user_id)
        return user_id
    except JWTError as e:
        # More specific error for JWT issues
        print(f"JWT Verification Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"JWT verification failed: {str(e)}",
        )
    except Exception as e:
        # Catch-all for other potential errors during decoding or UUID conversion
        # This might catch errors related to key loading if not a valid PEM.
        print(f"Authentication Exception: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
        )

async def get_current_user(user_id: UUID = Depends(authenticate_user)):
    return {"id": str(user_id)}

def get_current_user_id() -> UUID:
    """
    Retrieves the injected user_id from the context. 
    Must be called within an authenticated request.
    """
    uid = user_id_ctx.get()
    if not uid:
        raise RuntimeError("User context missing")
    return uid
