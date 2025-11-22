from pydantic import BaseModel

class JWTToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
    role: str | None = None