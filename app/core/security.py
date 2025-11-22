from enum import Enum

from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.models.user import UserRole

from .api_urls import TOKEN_FULL_PATH


class Permissions(str, Enum):
    READ_SELF = "read:self"
    WRITE_SELF = "write:self"

    READ_USERS = "read:users"
    WRITE_USERS = "write:users"
    DELETE_USERS = "delete:users"

    ADMIN = "admin"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=TOKEN_FULL_PATH,
    scopes={
        Permissions.READ_SELF: "Can read own user profile",
        Permissions.WRITE_SELF: "Can alter own user profile",
        Permissions.READ_USERS: "Read all users",
        Permissions.WRITE_USERS: "Add and update user",
        Permissions.DELETE_USERS: "Deactivate a user (soft delete)",
        Permissions.ADMIN: "Full Administrative Access",
    },
)

ROLE_SCOPES: dict[UserRole, list[Permissions]] = {
    UserRole.ADMIN: [
        Permissions.READ_SELF,
        Permissions.WRITE_SELF,
        Permissions.READ_USERS,
        Permissions.WRITE_USERS,
        Permissions.DELETE_USERS,
        Permissions.ADMIN,
    ],
    UserRole.USER: [Permissions.READ_SELF, Permissions.WRITE_SELF],
}

password_hash = PasswordHash.recommended()


def verify_password(plan_password, hashed_password):
    return password_hash.verify(plan_password, hashed_password)


def get_password_hash(plain_password):
    return password_hash.hash(plain_password)


def get_user_scopes(role: UserRole) -> list[str]:
    permissions = ROLE_SCOPES.get(role, [])
    return [perm.value for perm in permissions]
