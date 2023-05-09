from database import client, MONGO_DB_NAME
from datetime import datetime, date
from pymongo import ReturnDocument
from typing import Dict, Any

from schemas.user import *
from schemas.share import *

from fastapi.encoders import jsonable_encoder
import json
from bson import ObjectId
from pydantic import BaseModel
import bson


# custom encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, BaseModel):
            return obj.dict()
        else:
            return super().default(obj)


# Helpers


def rollbot_helper(rollbot) -> dict:
    return {
        "id": str(rollbot["_id"]),
        "name": str(rollbot["name"]),
        "number": int(rollbot["number"]),
        "image_url": str(rollbot["image_url"]),
        "stats": dict(rollbot["stats"]),
        "traits": dict(rollbot["traits"]),
    }


def sportbot_helper(sportbot) -> dict:
    return {
        "id": str(sportbot["_id"]),
        "name": str(sportbot["name"]),
        "number": int(sportbot["number"]),
        "image_url": str(sportbot["image_url"]),
        "stats": dict(sportbot["stats"]),
        "traits": dict(sportbot["traits"]),
    }


def share_helper(sport) -> dict:
    return {
        "id": str(sport["_id"]),
        "bots": int(sport["bots"]),
        "shares": int(sport["shares"]),
        "shareEntry": list[sport["shareEntry"]],
    }


# DB Helper
async def get_collection(collection_name):
    return client[MONGO_DB_NAME][collection_name]


async def create_document(collection_name, document):
    collection = await get_collection(collection_name)
    result = await collection.insert_one(document)
    return str(result.inserted_id)


async def get_documents(collection_name):
    collection = await get_collection(collection_name)
    documents = []
    async for document in collection.find({}):
        document["_id"] = str(document["_id"])
        documents.append(document)

    return documents


# by ID


async def get_document_by_id(collection_name, document_id):
    collection = await get_collection(collection_name)
    return await collection.find_one({"_id": ObjectId(document_id)})


# by Name


async def get_document_by_name(collection_name, document_name):
    collection = await get_collection(collection_name)
    document = await collection.find_one({"name": document_name})
    if document:
        document["_id"] = str(document["_id"])
    return document


# get Sport by sport


async def get_sport_by_sport(collection_name, sport):
    collection = await get_collection(collection_name)
    result = await collection.find_one({"sport": sport})
    if result:
        result["_id"] = str(result["_id"])
    return result


# update sport by sport


async def update_sport_by_sport(
    collection_name, sport: str, update_data: UpdateShareSchema
):
    collection = await get_collection(collection_name)
    sport_doc = await get_sport_by_sport(collection_name, sport)

    update_data_dict = update_data.dict(exclude_unset=True)

    if sport_doc is None:
        return "Sport not found!"

    result = await collection.update_one({"sport": sport}, {"$set": update_data_dict})

    if "sport" in update_data_dict:
        sport = update_data_dict["sport"]

    if result.modified_count == 1:
        # Return the updated document
        updated_sport_doc = await get_sport_by_sport(collection_name, sport)
        return updated_sport_doc

    return "sport not found or inventory is empty, or no user data was changed"


# Post Sport share
async def create_sport_share(collection_name, sport, share: list):
    collection = await get_collection(collection_name)
    sport_doc = await get_sport_by_sport(collection_name, sport)

    if sport_doc is not None:
        if not sport_doc["share_entrys"]:
            result = await collection.update_one(
                {"sport": sport}, {"$set": {"share_entrys": share}}
            )
            if result.modified_count == 1:
                updated_sport_doc = await get_sport_by_sport(collection_name, sport)
                return updated_sport_doc
        return {"Sport share list is not empty!"}
    return {"Sport not found"}


# sportbot by number


async def get_sportbot_by_number(collection_name, number):
    collection = await get_collection(collection_name)
    sportbot = await collection.find_one({"number": number})
    if sportbot:
        sportbot["_id"] = str(sportbot["_id"])
    return sportbot


# by username


async def get_document_by_username(collection_name, document_name):
    collection = await get_collection(collection_name)
    document = await collection.find_one({"username": document_name})
    if document:
        document["_id"] = str(document["_id"])
    return document


# hate dates


def date_to_datetime(d: date) -> datetime:
    return datetime(d.year, d.month, d.day, 0, 0, 0)


# get sport Shares


async def get_sport_shares(collection_name, sport):
    sport_ele = await get_sport_by_sport(collection_name, sport)

    if sport_ele is not None:
        result = sport_ele["share_entrys"]
        return result

    return {"sport not found"}


# get user inventory


async def get_user_inv(collection_name, username):
    # collection = await get_collection(collection_name)
    user = await get_document_by_username(collection_name, username)

    if user is not None:
        result = user["inventory"]

        return result

    return {"User is none"}


# create inv ( only works if inv is empty list)


async def create_user_inv(collection_name, username, inventory: list):
    collection = await get_collection(collection_name)
    user_doc = await get_document_by_username(collection_name, username)

    if user_doc is not None:
        if not user_doc["inventory"]:
            result = await collection.update_one(
                {"username": username}, {"$set": {"inventory": [inventory]}}
            )
            if result.modified_count == 1:
                updated_user_doc = await get_document_by_username(
                    collection_name, username
                )
                return updated_user_doc
        return {"User Inventory is not empty!"}
    return {"User not found"}


# update user data


async def update_user_by_username(
    collection_name, username: str, update_data: UpdateUserSchema
):
    collection = await get_collection(collection_name)
    user_doc = await get_document_by_username(collection_name, username)

    update_data_dict = update_data.dict(exclude_unset=True)

    if user_doc is None:
        return "User not found!"

    result = await collection.update_one(
        {"username": username}, {"$set": update_data_dict}
    )

    if "username" in update_data_dict:
        username = update_data_dict["username"]

    if result.modified_count == 1:
        # Return the updated document
        updated_user_doc = await get_document_by_username(collection_name, username)
        return updated_user_doc

    return "user not found or inventory is empty, or no user data was changed"


# update user inventory data


async def update_user_inventory_by_username(collection_name: str, username: str, item):
    collection = await get_collection(collection_name)
    user = await get_document_by_username(collection_name, username)

    bot_number = item.bot_number

    update_data = item.dict(exclude_unset=True)

    inventory = None

    user_inv = user["inventory"]

    if not isinstance(user_inv, list):
        user_inv = [user_inv]

    for inv in user_inv:
        if inv["bot_number"] == bot_number:
            print(inv["bot_number"])
            inventory = inv
            break

    if inventory is not None:
        new_data = {**inventory}

        if "bot" in update_data and update_data["bot"] is not None:
            new_data["bot"] = {
                **inventory["bot"],
                **{k: v for k, v in update_data["bot"].items() if v is not None},
            }

        if "stats" in update_data and update_data["bot"]["stats"] is not None:
            new_data["bot"]["stats"] = {
                **inventory["bot"]["stats"],
                **{
                    k: v
                    for k, v in update_data["bot"]["stats"].items()
                    if v is not None
                },
            }

        if "traits" in update_data and update_data["bot"]["traits"] is not None:
            new_data["bot"]["traits"] = {
                **inventory["bot"]["traits"],
                **{
                    k: v
                    for k, v in update_data["bot"]["traits"].items()
                    if v is not None
                },
            }

        if "value" in update_data and update_data["value"] is not None:
            new_data["value"] = update_data["value"]

        if "claimed" in update_data and update_data["claimed"] is not None:
            new_data["claimed"] = update_data["claimed"]

        if "claimed_at" in update_data and update_data["claimed_at"] is not None:
            new_data["claimed_at"] = update_data["claimed_at"]

        if "buy_price" in update_data and update_data["buy_price"] is not None:
            new_data["buy_price"] = update_data["buy_price"]

        if "unlocks_in" in update_data and update_data["unlocks_in"] is not None:
            new_data["unlocks_in"] = update_data["unlocks_in"]

        query = {"username": username}
        update_data = {"$set": {"inventory.$[i]": new_data}}
        array_filters = [{"i.bot_number": bot_number}]
        result = await collection.update_one(
            query, update_data, array_filters=array_filters
        )
        return {"User inventory data changed"}

    else:
        index = 0
        for i, b in enumerate(user["inventory"]):
            if b["bot_number"] > bot_number:
                index = i
                break
            else:
                index = i + 1

        query = {"username": username}
        update_data = {
            "$push": {"inventory": {"$each": [update_data], "$position": index}}
        }
        result = await collection.update_one(query, update_data)

        # result = await collection.update_one({"username": username}, {"$push": {"inventory": update_data}})
        return {"User inventory entry added"}


# delete inventory item


async def delete_item_from_user_inventory(
    collection_name: str, username: str, item_number: int
):
    collection = await get_collection(collection_name)

    user_inv = await get_user_inv(collection_name, username)

    for x in user_inv:
        if x["bot_number"] == item_number:
            result = await collection.update_one(
                {"username": username},
                {"$pull": {"inventory": {"bot_number": item_number}}},
            )

            if result.modified_count == 1:
                return {"deleted bot number", item_number}

            return {"Did not find bot with number", item_number}

    return {"Something went wrong"}


# by Sport


async def get_document_by_sport(collection_name, document_sport):
    collection = get_collection(collection_name)
    return collection.find_one({"sport": document_sport})


async def delete_document(collection_name, document_id):
    collection = get_collection(collection_name)
    return collection.delete_one({"_id": document_id})
