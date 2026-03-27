from fastapi import Header, HTTPException
import jwt
from jwt import PyJWKClient
from app.core.config import get_settings

_jwks_client = None

def get_jwks_client():
    global _jwks_client
    if _jwks_client is None:
        jwks_url = f"{get_settings().supabase_url}/auth/v1/.well-known/jwks.json"
        _jwks_client = PyJWKClient(jwks_url)
    return _jwks_client

async def get_current_user_id(authorization: str = Header(...)) -> str:
    """Extract user UUID from Supabase JWT."""
    try:
        token = authorization.split(" ")[1]
        signing_key = get_jwks_client().get_signing_key_from_jwt(token)
        
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated"
        )
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    

