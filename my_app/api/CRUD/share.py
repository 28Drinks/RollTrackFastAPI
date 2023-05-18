from database import client, MONGO_DB_NAME, TEST_MONGO_DB_NAME
import re

from schemas.inventory import *
from bson import ObjectId

collection_name = "shares"
collection = client[TEST_MONGO_DB_NAME][collection_name]


async def get_all_share(sport, date):
    match_stage = {}
    if sport:
        #sport = sport.lower()
        match_stage["sport"] = sport
    if date:
        pattern = re.compile(f"^{date}")
        match_stage["date_time"] = {"$regex": pattern}
    
    pipeline = [
        {"$match": match_stage},
        {"$sort": {"value": -1}},
        {"$project": {"_id": 0}}
    ]
    cursor = collection.aggregate(pipeline)
    result = await cursor.to_list(length=None)
    return result


async def get_share_by_sport(sport):
    cursor = collection.find({"sport": sport})
    result = await cursor.to_list(length=None)
    for doc in result:
        doc["_id"] = str(doc["_id"])
    return result


async def get_share_by_day(share_date):
    pattern = re.compile(f"^{share_date}")
    query = {"date_time": {"$regex": pattern}}
    cursor = collection.find(query)
    result = await cursor.to_list(length=None)
    for doc in result:
        doc["_id"] = str(doc["_id"])
    return result