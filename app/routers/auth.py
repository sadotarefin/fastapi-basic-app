from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from ..core.api_urls import AUTH_PREFIX, TOKEN


router = APIRouter(
    prefix=AUTH_PREFIX
)

print(AUTH_PREFIX, TOKEN)

@router.post(TOKEN)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": "hellotoken", "token_type": "bearer"}