from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from ..core.api_urls import USERS_PREFIX
from ..models.user import User
from ..schemas.user import UserCreate, UserPublic
from ..services.user_service import UserService
from ..core.security import oauth2_scheme
from ..db.db import SessionDep

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

@router.post("/", response_model=UserPublic)
async def create_user(session: SessionDep, data: UserCreate):
    try:
        user = UserService.register_user(session, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        
        



