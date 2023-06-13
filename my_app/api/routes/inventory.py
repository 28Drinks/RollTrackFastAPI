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
    user_inventory = await get_current_user_inventoy(user_id)
    return user_inventory


# create the users inventory, if he has none, and set its id to the user. Retunr the id
@inventory.post("/inventory/")
async def post_inventory_me(inventory_data: UserIventorySchema, current_user: UserSchema = Depends(get_current_user)) :
    user_id = current_user["_id"]
    user_inventory = await get_current_user_inventoy(user_id)
    if user_inventory:
        return "User already has an inventory"
    inventory_doc = await post_current_user_inventory(user_id, inventory_data)
    add_inv_id_to_user = await update_user(user_id, {"inventory_id": inventory_doc["_id"]})
    return add_inv_id_to_user


@inventory.put("/inventory/")
async def add_bot_to_inventory(new_inventory_entry: AddInventoryEntrySchema, current_user: UserSchema = Depends(get_current_user)):
    user_id = current_user["_id"]
    updated_inventory = await add_bot_to_inv(user_id, new_inventory_entry)
    return updated_inventory


@inventory.put("/inventory/{bot_id}")
async def update_bot_in_inventory(bot_id: str, bot_update: UpdateBot, current_user: UserSchema = Depends(get_current_user)):
    user_id = current_user["_id"]
    updated_bot = await update_bot_in_inventory(user_id, bot_id, bot_update)
    return updated_bot


@inventory.delete("/inventory/")
async def delete_inventory_me(bot_id: str, current_user: UserSchema = Depends(get_current_user)):
    user_id = current_user["_id"]
    deleted_inventory_entry = await delete_current_user_inventory(user_id, bot_id)
    return deleted_inventory_entry