from sqlmodel import Session
from datetime import datetime, timedelta, timezone
from app.core.config import Settings, SettingsDep
from app.db.db import SessionDep
from app.exceptions.exception_handler import CredentialException
from app.schemas.user import UserPublic
from app.crud.user import UserCrud
from app.core.security import password_hash
from app.core.security import oauth2_scheme
import jwt
from jwt.exceptions import InvalidTokenError
from typing_extensions import Annotated

from fastapi import Depends


class AuthService:

    @staticmethod 
    def verify_password(plan_password, hashed_password):
        return password_hash.verify(plan_password, hashed_password)
    
    @staticmethod
    def get_user(session: Session, username: str, password:str) -> UserPublic:
        user_in_db = UserCrud.get_by_username(session, username=username)
        
        if not user_in_db:
            raise CredentialException()
        
        if not AuthService.verify_password(password, user_in_db.hashed_password):
            raise CredentialException()
        
        return user_in_db
    
    @staticmethod
    async def prepare_access_token(settings: Settings, user: UserPublic):    
        access_token_expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + access_token_expires_delta
        to_encode = {
            "sub": user.username
        }
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=[settings.ALGORITHM])
        return encode_jwt
    
    @staticmethod
    async def get_current_user(settings: SettingsDep, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            if not username:
                raise CredentialException()
        except InvalidTokenError:
            raise CredentialException()
        
        user_in_db = UserCrud.get_by_username(session, username=username)
        
        return user_in_db


        
        

        