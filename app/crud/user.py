from sqlmodel import select, Session, or_
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

class UserCrud:
    @staticmethod
    def create_user(session: Session, data: UserCreate, password: str):
        print(data.model_dump())
        user = User(**data.model_dump(), hashed_password=password)
        model = User.model_validate(user)
        session.add(model)
        session.commit()
        session.refresh(model)
        return model
    
    @staticmethod
    def get_all(session: Session, offset: 0, limit: 100):
        return session.exec(
            select(User).order_by(User.id).offset(offset).limit(limit)
        ).all()
    
    @staticmethod
    def get_by_username(session: Session, username: str):
        return session.exec(
            select(User).where(User.username==username)
        ).first()
    
    @staticmethod
    def get_by_username_or_email(session: Session, username: str, email: str):
        return session.exec(
            select(User).where(or_(
                User.username==username,
                User.email==email
            ))
        ).first()
    
    @staticmethod
    def get(session: Session, user_id):
        return session.get(User, user_id)
    
    @staticmethod  #only patch
    def update(session, user_id, data: UserUpdate): 
        user_db = session.get(User, user_id)
        user_data = data.model_dump(exclude_unset=True)
        user_db.sqlmodel_update(user_data)

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db

