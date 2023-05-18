from database import client, MONGO_DB_NAME, TEST_MONGO_DB_NAME

from schemas.inventory import *
from CRUD.share import *
from bson import ObjectId

collection_name = "sportbots"
collection = client[TEST_MONGO_DB_NAME][collection_name]


async def get_sportbot_by_number(number):
    result = await collection.find_one({"number": number})
    if result:
        result["_id"] = str(result["_id"])
    if result["revealed"] == False:
        return result
    sport = result["sport"]
    shares = result["sportshares"]
    pipeline = [
        {"$match": {"sport": sport}},
        {"$limit": 1}
    ]
    share_result_cursor = client[TEST_MONGO_DB_NAME]["shares"].aggregate(pipeline)
    share_result = await share_result_cursor.to_list(length=None)
    result["share"] = ( share_result[0]["value"] * shares )
    return result

