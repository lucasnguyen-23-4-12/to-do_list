from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic import ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    # bcrypt chỉ hỗ trợ tối đa 72 bytes, nên giới hạn độ dài
    password: str = Field(..., min_length=6, max_length=72)


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None