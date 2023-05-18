from database import client, MONGO_DB_NAME, TEST_MONGO_DB_NAME

from schemas.inventory import *
from bson import ObjectId

collection_name = "sportbots"
collection = client[TEST_MONGO_DB_NAME][collection_name]


async def get_sportbot_by_number(number):
    result = await collection.find_one({"number": number})
    if result:
        result["_id"] = str(result["_id"])
    return result

