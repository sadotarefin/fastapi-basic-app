from sqlmodel import Session

from app.core.security import get_password_hash
from app.crud.user import UserCrud
from app.exceptions.exception_handler import ConflictException
from app.schemas.user import UserCreate, UserPublic


class UserService:

    @staticmethod
    def register_user(session: Session, data: UserCreate)->UserPublic:
        user = UserCrud.get_by_username_or_email(session, data.username, data.email)
        if user:
            raise ConflictException()
        password = get_password_hash(data.password)
        return UserCrud.create_user(session, data, password=password)
    
    @staticmethod
    def get_all_user(session: Session, offset, limit)->list[UserPublic]:
        #TODO: This can be replaced with windows function to read results and totals using one single query.
        total = UserCrud.count_users(session) 
        return UserCrud.get_all(session, offset, limit), total
