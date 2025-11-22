from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse


class ReferenceException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class NotFoundException(HTTPException):
    """404 Not Found"""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ForbiddenException(HTTPException):
    """403 Forbidden"""

    def __init__(
        self, detail: str = "Operation is not permitted", headers: dict | str = None
    ):
        if isinstance(headers, str):
            headers = {"WWW-Authenticate": headers}
        elif headers is None:
            headers = {"WWW-Authenticate": "Bearer"}

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers=headers,
        )


class CustomTokenException(HTTPException):
    """Custom token-related exceptions"""

    def __init__(
        self,
        message: str,
        header: str = "Bearer",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(
            status_code=status_code,
            detail=message,
            headers={"WWW-Authenticate": header},
        )


class CredentialException(HTTPException):
    """401 Unauthorized"""

    def __init__(
        self, detail: str = "Could not validate credentials", headers: dict | str = None
    ):
        if isinstance(headers, str):
            headers = {"WWW-Authenticate": headers}
        elif headers is None:
            headers = {"WWW-Authenticate": "Bearer"}

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


async def reference_exception_handler(
    request: Request, exc: ReferenceException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT, content={"detail": "I am teapot!!!!"}
    )
