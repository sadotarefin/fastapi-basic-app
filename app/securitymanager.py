from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix="/auth"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{router.prefix}/token")

@router.post("/token")
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": "hellotoken", "token_type": "bearer"}

