from .base_sql_model import BaseSqlModel
from pydantic import EmailStr
from enum import Enum

from sqlmodel import SQLModel, Field

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(SQLModel):
    username: str = Field(index=True, max_length=20, unique=True)
    email: EmailStr = Field(index=True, max_length=80, unique=True)
    full_name: str | None = Field(default=None, max_length=40)
    role: UserRole = Field(default=UserRole.USER)


class User(BaseSqlModel, UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    disabled: bool = False
