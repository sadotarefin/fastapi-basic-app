from sqlmodel import select

from app.core.security import password_hash
from app.models.user import User, UserRole


def create_seed_data(session, settings):
    user_exists = session.exec(
        select(User).where(User.username == settings.ADMIN_USERNAME)
    ).first()

    if user_exists:
        print("admin user already exists!")
        return

    admin_user = {
        "username": settings.ADMIN_USERNAME,
        "email": settings.ADMIN_EMAIL,
        "full_name": settings.ADMIN_FULL_NAME,
        "hashed_password": password_hash.hash(settings.ADMIN_PASS),
        "role": UserRole.ADMIN,
    }

    user = User(**admin_user)

    session.add(user)
    session.commit()
