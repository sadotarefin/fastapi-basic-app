from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import select
from ..core.api_urls import USERS_PREFIX
from ..models.user import User
from ..schemas.user import UserPublic
from ..core.security import oauth2_scheme
from ..core.db import SessionDep

router = APIRouter(
    prefix=USERS_PREFIX,
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=list[UserPublic])
async def read_users(session: SessionDep):
    return session.exec(select(User)).all()

@router.get("/me")
async def read_user_me(token: Annotated[str, Depends(oauth2_scheme)]):
    return {
        "username": "fakecurrentuser",
    }

@router.get("/{user_id}")
async def read_user(user_id: str):
    return {
        "username": f"{user_id}_user",
    }


