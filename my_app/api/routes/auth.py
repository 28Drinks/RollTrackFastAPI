from datetime import datetime, timedelta
from fastapi import APIRouter, Body, HTTPException, Depends, Header, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from schemas.user import *
from schemas.util import *

from db_helper import (
    create_document,
    get_document_by_id,
    get_document_by_name,
    get_document_by_sport,
    get_documents,
    get_document_by_username,
)

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


auth = APIRouter()

collection_name = "user_collection"


async def add_user_data(
    collection_name: str = collection_name, user: UserSchema = Body(...)
):
    user = jsonable_encoder(user)
    new_user = await create_document(collection_name, user)
    print(new_user)
    return


async def get_user_by_name(username, collection_name: str = collection_name):
    user = await get_document_by_username(collection_name, username)
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    username = to_encode["sub"]
    to_encode.update({"username": username})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Header(...)):
    if not token:
        raise HTTPException(status_code=401, detail="No token")
    print("Getting current user...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload["username"]
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )

    user = await get_user_by_name(username)
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@auth.post("/register")
async def register(user: UserSchema):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict["hashed_password"])
    existing_user = await get_user_by_name(user_dict["username"])
    print(await get_user_by_name(user_dict["username"]))
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    await add_user_data(user=user_dict)
    return {"detail": "User registered successfully"}


@auth.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_name(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password 1")
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password 2")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"token": access_token}


@auth.get("/users/me")
async def get_current_user_me(current_user: UserSchema = Depends(get_current_user)):
    print(current_user)

    return current_user
