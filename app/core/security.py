from fastapi.security import OAuth2PasswordBearer
from .api_urls import TOKEN_FULL_PATH

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_FULL_PATH)