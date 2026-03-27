from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, List, Dict, Any
from uuid import UUID
from datetime import datetime

# --- AUTH & USER SCHEMAS ---
class UserProfileResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

