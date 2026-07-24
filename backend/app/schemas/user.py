from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    target_exam_date: Optional[datetime] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    target_exam_date: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class GuestProgressItem(BaseModel):
    node_key: str
    mastery_level: float = 50.0
    streak_days: int = 1

class SessionMigrationRequest(BaseModel):
    guest_progress: List[GuestProgressItem] = []
    tbs_code: Optional[str] = None
    tbs_rows: Optional[List[Dict[str, Any]]] = None

class QRSessionResponse(BaseModel):
    qr_token: str
    auth_token: str
    qr_url: str
