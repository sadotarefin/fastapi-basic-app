from typing_extensions import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from .routers import auth, users
from .core.config import Settings, get_app_settings
from .core.db import create_db_and_tables, get_session
from .core.init_db import create_seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    create_seed_data(next(get_session()),get_app_settings())
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_app_settings)]):
    return {"message": "Hello Bigger Application"}
