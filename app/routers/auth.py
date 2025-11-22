from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import SettingsDep
from app.schemas.auth import JWTToken
from app.db.db import SessionDep
from app.services.auth_service import AuthService

from app.core.api_urls import AUTH_PREFIX, TOKEN

router = APIRouter(prefix=AUTH_PREFIX)


@router.post(TOKEN)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    settings: SettingsDep,
):
    user = AuthService.get_user(
        session, form_data.username, form_data.password
    )  # exception should be already handled now.
    scopes = AuthService.negotiate_scopes(user, form_data.scopes)
    access_token = await AuthService.prepare_access_token(settings, user, scopes)
    token = JWTToken(access_token=access_token, token_type="bearer")

    return token
