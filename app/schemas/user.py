from datetime import datetime
from sqlmodel import SQLModel
from app.models.user import UserBase
from pydantic import EmailStr, Field

class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=80)
    full_name: str | None = Field(default=None, max_length=40)
