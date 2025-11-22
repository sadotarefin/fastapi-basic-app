from datetime import datetime, timedelta, timezone

from fastapi.security import SecurityScopes
import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session
from typing_extensions import Annotated

from app.core.config import Settings, SettingsDep
from app.core.security import get_user_scopes, oauth2_scheme, verify_password
from app.crud.user import UserCrud
from app.db.db import SessionDep
from app.exceptions.exception_handler import CredentialException
from app.schemas.auth import TokenData
from app.schemas.user import UserPublic


class AuthService:
    @staticmethod
    def get_user(session: Session, username: str, password: str) -> UserPublic:
        user_in_db = UserCrud.get_by_username(session, username=username)

        if not user_in_db:
            raise CredentialException()

        if not verify_password(password, user_in_db.hashed_password):
            raise CredentialException()

        return user_in_db

    @staticmethod
    def negotiate_scopes(user: UserPublic, requested_scopes: list[str]) -> list[str]:
        allowed_scopes = get_user_scopes(user.role)

        if not requested_scopes:
            return allowed_scopes

        granted_scopes = [
            scope for scope in requested_scopes if scope in allowed_scopes
        ]

        return granted_scopes

    @staticmethod
    async def prepare_access_token(
        settings: Settings, user: UserPublic, scopes: list[str]
    ):
        access_token_expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        expire = datetime.now(timezone.utc) + access_token_expires_delta

        to_encode = {
            "sub": user.username,
            "role": user.role.value,
            "scopes": " ".join(scopes),
            "exp": expire,
        }

        encode_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

        return encode_jwt

    @staticmethod
    async def get_current_user(
        security_scopes: SecurityScopes,
        settings: SettingsDep,
        session: SessionDep,
        token: Annotated[str, Depends(oauth2_scheme)],
    ):
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username = payload.get("sub")
            if not username:
                raise CredentialException(headers=authenticate_value)
            scope: str = payload.get("scope", " ")
            token_scopes = scope.split(" ")
            token_data = TokenData(username=username, scopes=token_scopes)
        except InvalidTokenError:
            raise CredentialException(headers=authenticate_value)

        user_in_db = UserCrud.get_by_username(session, username=username)
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes and scope not in get_user_scopes(
                user_in_db.role
            ):
                raise CredentialException(authenticate_value)

        return user_in_db
