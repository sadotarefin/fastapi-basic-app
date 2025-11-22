from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from typing_extensions import Annotated

from app.exceptions.exception_handler import (
    ReferenceException,
    reference_exception_handler,
)

from .core.config import Settings, get_app_settings
from .db.db import create_db_and_tables, get_session
from .db.init_db import create_seed_data
from .routers import auth, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    create_seed_data(next(get_session()), get_app_settings())
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)

app.add_exception_handler(ReferenceException, reference_exception_handler)


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_app_settings)]):
    return {"message": "Hello Bigger Application"}
