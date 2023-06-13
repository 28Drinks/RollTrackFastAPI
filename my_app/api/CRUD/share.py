from database import client, MONGO_DB_NAME, TEST_MONGO_DB_NAME
import re

from schemas.inventory import *
from bson import ObjectId

collection_name = "shares"
collection = client[TEST_MONGO_DB_NAME][collection_name]


async def get_all_share(sport, date, limit):
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
    if limit:
        pipeline.append({"$limit": limit})
    cursor = collection.aggregate(pipeline)
    result = await cursor.to_list(length=None)
    return result