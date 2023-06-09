from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from routes.sportbots import sportbots
from routes.share import share
from routes.user import user
from routes.auth import auth
from routes.inventory import inventory

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


origins = [
    "http://167.172.166.15:8000",
    "http://167.172.166.15:80",
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(sportbots, prefix="/api", tags=["Sportbots"])
app.include_router(share, prefix="/api", tags=["Share"])
app.include_router(user, prefix="/api", tags=["User"])
app.include_router(auth, prefix="/api", tags=["Auth"])
app.include_router(inventory, prefix="/api", tags=["Inv"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
