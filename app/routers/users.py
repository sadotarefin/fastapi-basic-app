from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.core.api_urls import USERS_PREFIX 
from app.schemas.user import UserCreate, UserPublic
from app.services.user_service import UserService
from app.services.auth_service import AuthService
#from ..core.security import oauth2_scheme
from app.db.db import SessionDep

router = APIRouter(
    prefix=USERS_PREFIX,
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=list[UserPublic])
async def read_users(session: SessionDep, offset: Annotated[int, Query(ge=0)]=0, limit: Annotated[int, Query(ge=1)] = 100):
    return UserService.get_all_user(session, offset, limit)

@router.get("/me", response_model=UserPublic)
async def read_user_me(current_user: Annotated[str, Depends(AuthService.get_current_user)]):
    return current_user

@router.get("/{user_id}")
async def read_user(user_id: str):
    return {
        "username": f"{user_id}_user",
    }

@router.post("/", response_model=UserPublic)
async def create_user(session: SessionDep, data: UserCreate):
    return UserService.register_user(session, data)
        
        



