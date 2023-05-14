from datetime import datetime, timedelta
from fastapi import APIRouter, Body, HTTPException, Depends, Header, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from schemas.user import *
from schemas.util import *
from CRUD.auth import *

auth = APIRouter()

collection_name = "user_collection"


@auth.post("/register")
async def register(user: UserSchema):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict["hashed_password"])
    existing_user = await get_user_by_name(user_dict["username"])
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    await post_user(user_dict)
    return {"detail": "User registered successfully"}


@auth.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_name(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password 1")
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password 2")
    access_token = create_access_token(
        data={"_id": str(user["_id"])},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"token": access_token}


@auth.get("/users/me")
async def get_current_user_me(current_user: UserSchema = Depends(get_current_user)):

    return current_user
