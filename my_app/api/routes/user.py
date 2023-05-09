from datetime import datetime, timedelta
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from pydantic import parse_obj_as
from typing import Dict, Any

from schemas.user import *
from schemas.util import *

from db_helper import (
    create_document,
    get_document_by_id,
    get_document_by_name,
    get_document_by_sport,
    get_documents,
    get_document_by_username,
    update_user_by_username,
    create_user_inv,
    update_user_inventory_by_username,
    get_user_inv,
    delete_item_from_user_inventory,
)

import json
from bson.objectid import ObjectId

user = APIRouter()

collection_name = "user_collection"


@user.get("/user/")
async def get_user(collection_name: str = collection_name):
    user = await get_documents(collection_name)
    if user:
        return ResponseModel(user, "User successfulyl retrieved from db")
    return ResponseModel(user, "Empty list returned")


@user.get("/user/{name}")
async def get_user_by_name(username: str, collection_name: str = collection_name):
    user = await get_document_by_username(collection_name, username)
    if user:
        return ResponseModel(
            user, "Successfully retrived User {} from DB".format(username)
        )
    return ErrorResponseModel("Error", 404, "Something went wrong retrieved from db")


# @user.post("/user/")
# async def add_user_data(collection_name: str = collection_name, user: UserSchema = Body(...)):
#     user = jsonable_encoder(user)
#     new_user = await create_document(collection_name, user)
#     print(new_user)
#     return ResponseModel(new_user, "User added succesfully")


@user.put("/user/{username}")
async def update_user_data(
    username, update_data: ReadUserSchema, collection_name: str = collection_name
):
    user = await get_document_by_username(collection_name, username)
    if user is None:
        return {"User not found"}

    updated_user = await update_user_by_username(
        collection_name, user["username"], update_data
    )
    if updated_user is None:
        return {"update failed"}

    return updated_user


# Inventory


@user.get("/user/{username}/inventory")
async def get_inventory(username: str, collection_name: str = collection_name):
    user = await get_document_by_username(collection_name, username)
    if user is None:
        return {"User not found"}

    get_inv = await get_user_inv(collection_name, user["username"])
    if get_inv is None:
        return {"Inventory get is none"}

    return get_inv


@user.post("/user/{username}/inventory")
async def add_inventory(
    username: str, inventory: InventorySchema, collection_name: str = collection_name
):
    inventory = jsonable_encoder(inventory)
    user = await get_document_by_username(collection_name, username)
    if user is None:
        return {"User not found"}

    post_inv = await create_user_inv(collection_name, user["username"], inventory)
    if post_inv is None:
        return {"Inv post failed"}

    return user, post_inv


@user.put("/user/{username}/inventory")
async def add_item_to_inventory(
    username: str, item: UpdateInventorySchema, collection_name: str = collection_name
):
    print(item)

    user = await get_document_by_username(collection_name, username)
    if user is None:
        return {"User not found"}

    updated_user = await update_user_inventory_by_username(
        collection_name, user["username"], item
    )
    if updated_user is None:
        return {"update failed"}

    return updated_user


@user.delete("/user/{username}/inventory/{item_number}")
async def delete_item_from_inventory(
    username: str, item_number: int, collection_name: str = collection_name
):
    print(item_number)

    user = await get_document_by_username(collection_name, username)
    if user is None:
        return {"User not found"}

    deleted_item = await delete_item_from_user_inventory(
        collection_name, user["username"], item_number
    )
    if deleted_item is None:
        return {"Delelte item failed"}

    return deleted_item
