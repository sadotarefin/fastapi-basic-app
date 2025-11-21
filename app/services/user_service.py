from sqlmodel import Session
from app.crud.user import UserCrud
from app.schemas.user import UserCreate, UserPublic
from ..core.security import password_hash

class UserService:

    @staticmethod
    def register_user(session: Session, data: UserCreate)->UserPublic:
        user = UserCrud.get_by_username_or_email(session, data.username, data.email)
        if user:
            raise ValueError("Username or email already taken")
        password = password_hash.hash(data.password)
        return UserCrud.create_user(session, data, password=password)
