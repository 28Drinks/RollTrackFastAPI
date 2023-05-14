from datetime import datetime, timedelta
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json
from bson.objectid import ObjectId
from pydantic import parse_obj_as
from typing import Dict, Any

from schemas.user import *
from schemas.util import *

from CRUD.user import *


user = APIRouter()


@user.get("/users/")
async def get_user():
    users = await get_users()
    if users:
        return ResponseModel(users, "Users successfulyl retrieved from db")
    return ResponseModel(users, "Empty list returned")


@user.get("/user/{username}")
async def get_user_by_username(username: str):
    user = await get_user_by_name(username)
    if user:
        return ResponseModel(
            user, "Successfully retrived User {} from DB".format(username)
        )
    return ErrorResponseModel("Error", 404, "Something went wrong retrieved from db")


@user.post("/user/")
async def add_user_data(user: UserSchema = Body(...)):
    user_data = jsonable_encoder(user)
    new_user = await post_user(user_data)
    return ResponseModel(new_user, "User added succesfully")


@user.put("/user/{username}")
async def update_user_data(username, update_data: dict):

    updated_user = await update_user(username, update_data)
    if updated_user is None:
        return {"update failed"}

    return updated_user


@user.delete("/user/{username}")
async def delete_user(username):
    user_to_delete = await get_user_by_name(username)
    if user_to_delete is None:
        return {"User not found"}

    deleted_user = await delete_user(user_to_delete["_id"])

    return deleted_user
