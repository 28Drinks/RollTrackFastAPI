from database import client, MONGO_DB_NAME

from schemas.inventory import *
from bson import ObjectId

collection_name = "inventory_collection"
collection = client[MONGO_DB_NAME][collection_name]

async def get_current_user_inventoy(user_id):
    result = await collection.find_one({"user_id": user_id})
    result["_id"] = str(result["_id"])
    return result


async def post_current_user_inventory(user_id, document):
    print(document.dict())
    result = await collection.insert_one(document.dict())
    inserted_id = result.inserted_id
    inventory_doc = await collection.find_one({"_id": inserted_id})
    inventory_doc["_id"] = str(inventory_doc["_id"])
    return inventory_doc

async def add_bot_to_inv(user_id, document):
    inventory_to_update = await get_current_user_inventoy(user_id)

    if inventory_to_update:

        result = await collection.update_one(
            {"user_id": user_id}, 
            {"$push": {"bots": document.dict()}}
            )
        if result.modified_count > 0:
            return "Added new bot to inventory"
        return "Failed to add new bot to inventory"
    return "Inventory not found"


async def update_bot_in_inventory(user_id, bot_id, bot_update):
    inventory = await collection.find_one({"user_id": user_id})
    if inventory is None:
        return "Inventory not found"
    inventory_bots = inventory.get("bots", [])
    for bot in inventory_bots:
        if bot["bot_id"] == bot_id:
            bot.update(bot_update)
            result = await collection.update_one(
                {"user_id": user_id},
                {"$set": {"bots": inventory_bots}}
            )
            if result.modified_count > 0:
                return "Successfully updated the bot"
            return "Failed to update the bot"
    return "Bot not found in inventory"

async def delete_current_user_inventory(user_id, bot_id):

    inventory = await get_current_user_inventoy(user_id)

    print(inventory)

    if inventory:
        result = await collection.update_one(
            {"user_id": user_id},
            {"$pull": {"bots": {"bot_id": bot_id}}}
        )
        if result.modified_count > 0:
            return f"Deleted bot with ID {bot_id}"
        return f"Bot with ID {bot_id} not found."
    return "inventory not found"