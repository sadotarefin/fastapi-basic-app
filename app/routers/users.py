from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.api_urls import USERS_PREFIX 
from app.schemas.user import UserCreate, UserPublic
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.db.db import SessionDep

router = APIRouter(
    prefix=USERS_PREFIX,
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=PaginatedResponse[UserPublic])
def read_users(session: SessionDep, filter_query: Annotated[PaginationParams, Query()]):
    print(filter_query)
    items, total = UserService.get_all_user(session, filter_query.offset, filter_query.limit)
    return PaginatedResponse(items=items, total=total, offset=filter_query.offset, limit=filter_query.limit)

@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: Annotated[UserPublic, Depends(AuthService.get_current_user)]):
    return current_user

@router.get("/{user_id}")
def read_user(user_id: str):
    return {
        "username": f"{user_id}_user",
    }

@router.post("/", response_model=UserPublic)
def create_user(session: SessionDep, data: UserCreate):
    return UserService.register_user(session, data)
        
        



