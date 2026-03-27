import pytest
from uuid import uuid4
import jwt
from fastapi import HTTPException
from app.core.auth import authenticate_user
from fastapi.security import HTTPAuthorizationCredentials
from app.core.config import get_settings

settings = get_settings()

def create_token(user_id: str):
    payload = {"sub": user_id}
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")

@pytest.mark.asyncio
async def test_authenticate_user_success():
    user_id = str(uuid4())
    token = create_token(user_id)
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    
    result = await authenticate_user(creds)
    assert str(result) == user_id

@pytest.mark.asyncio
async def test_authenticate_user_failure():
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid-token")
    
    with pytest.raises(HTTPException) as excinfo:
        await authenticate_user(creds)
    assert excinfo.value.status_code == 401
