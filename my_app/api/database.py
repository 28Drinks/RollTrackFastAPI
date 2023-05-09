from datetime import datetime
from pydantic import BaseModel
from decouple import config
import motor.motor_asyncio

MONGO_DETAILS = config("MONGO_DETAILS")
MONGO_DB_NAME = "testing2"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, serverSelectionTimeoutMS=5000)


rollbots_collection = client[MONGO_DB_NAME]["rollbots_collection"]
sportbots_collection = client[MONGO_DB_NAME]["sportbots_collection"]
share_collection = client[MONGO_DB_NAME]["share_collection"]
user_collection = client[MONGO_DB_NAME]["user_collection"]
