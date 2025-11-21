from fastapi import Request, status
from fastapi.responses import JSONResponse

class CredentialException(Exception):
    def __init__(self):
        self.message = f"Wrong credentials"
        super().__init__(self.message)

class ConflictException(Exception):
    def __init__(self):
        self.message = f"The resource you are creating may conflict with existing resource"
        super().__init__(self.message)

async def credential_exception_handler(request: Request, exc: CredentialException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"}
    )

async def conflict_exception_handler(request: Request, exc: ConflictException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message} 
    )

 