from .base_sql_model import BaseSqlModel
from pydantic import EmailStr

from sqlmodel import Field

class UserBase(BaseSqlModel):
    username: str = Field(index=True, max_length=12)
    email: EmailStr | None = Field(default=None, max_length=80)
    full_name: str | None = Field(default=None, max_length=40)
    disabled: bool = False

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
