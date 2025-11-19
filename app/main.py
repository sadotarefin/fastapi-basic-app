from fastapi import FastAPI

from .routers import users
from .securitymanager import router as securityrouter

app = FastAPI()

app.include_router(securityrouter)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Application"}
