from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import SettingsDep
from ..schemas.auth import JWTToken
from ..db.db import SessionDep
from ..services.auth_service import AuthService

from ..core.api_urls import AUTH_PREFIX, TOKEN

router = APIRouter(
    prefix=AUTH_PREFIX
)

@router.post(TOKEN)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep, settings: SettingsDep):
    user = AuthService.get_user(session, form_data.username, form_data.password) #exception should be already handled now.

    token = JWTToken(access_token=await AuthService.preapre_access_token(settings, user), token_type="bearer")

    return token