from datetime import datetime, timedelta
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json
from bson.objectid import ObjectId
from pydantic import parse_obj_as
from typing import Dict, Any

from schemas.user import *
from schemas.inventory import *
from schemas.util import *

from CRUD.auth import *
from CRUD.user import *
from CRUD.inventory import *


inventory = APIRouter()

@inventory.get("/inventory/me/")
async def get_inventory_me(current_user: UserSchema = Depends(get_current_user)):
    user_id = current_user["_id"]

    inventory = await get_current_user_inventoy(user_id)
    return inventory


@inventory.post("/inventory/me/")
async def post_inventory_me(inventory_data: UserIventorySchema, current_user: UserSchema = Depends(get_current_user)) :
    user_id = current_user["_id"]
    inventory_doc = await post_current_user_inventory(user_id, inventory_data)
    
    add_inv_id_to_user = await update_user(user_id, {"inventory_id": inventory_doc["_id"]})
    return inventory


@inventory.put("/inventory/me/")
async def add_bot_to_inventory(new_inventory_entry: AddInventoryEntrySchema, current_user: UserSchema = Depends(get_current_user)):
    user_id = current_user["_id"]

    updated_inventory = await add_bot_to_inv(user_id, new_inventory_entry)
    return updated_inventory


@inventory.put("/inventory/me/{bot_id}")
async def update_bot_in_inventory(bot_id: str, bot_update: UpdateBot, current_user: UserSchema = Depends(get_current_user)):
    user_id = current_user["_id"]

    updated_bot = await update_bot_in_inventory(user_id, bot_id, bot_update)
    return updated_bot

@inventory.delete("/inventory/me")
async def delete_inventory_me(bot_id: str, current_user: UserSchema = Depends(get_current_user)):
    user_id = current_user["_id"]

    deleted_inventory_entry = await delete_current_user_inventory(user_id, bot_id)
    return deleted_inventory_entry



# Inventory

# @user.get("/user/{username}/inventory")
# async def get_inventory(username: str, collection_name: str = collection_name):
#     user = await get_document_by_username(collection_name, username)
#     if user is None:
#         return {"User not found"}

#     get_inv = await get_user_inv(collection_name, user["username"])
#     if get_inv is None:
#         return {"Inventory get is none"}

#     return get_inv


# @user.post("/user/{username}/inventory")
# async def add_inventory(
#     username: str, inventory: InventorySchema, collection_name: str = collection_name
# ):
#     inventory = jsonable_encoder(inventory)
#     user = await get_document_by_username(collection_name, username)
#     if user is None:
#         return {"User not found"}

#     post_inv = await create_user_inv(collection_name, user["username"], inventory)
#     if post_inv is None:
#         return {"Inv post failed"}

#     return user, post_inv


# @user.put("/user/{username}/inventory")
# async def add_item_to_inventory(
#     username: str, item: UpdateInventorySchema, collection_name: str = collection_name
# ):
#     print(item)

#     user = await get_document_by_username(collection_name, username)
#     if user is None:
#         return {"User not found"}

#     updated_user = await update_user_inventory_by_username(
#         collection_name, user["username"], item
#     )
#     if updated_user is None:
#         return {"update failed"}

#     return updated_user


# @user.delete("/user/{username}/inventory/{item_number}")
# async def delete_item_from_inventory(
#     username: str, item_number: int, collection_name: str = collection_name
# ):
#     print(item_number)

#     user = await get_document_by_username(collection_name, username)
#     if user is None:
#         return {"User not found"}

#     deleted_item = await delete_item_from_user_inventory(
#         collection_name, user["username"], item_number
#     )
#     if deleted_item is None:
#         return {"Delelte item failed"}

#     return deleted_item