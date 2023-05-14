from datetime import datetime, timedelta
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from schemas.rollbots import *
from schemas.util import *

rollbots = APIRouter()

collection_name = "rollbots_collection"


@rollbots.get("/rollbot/")
async def get_rollbots(
    collection_name: str = collection_name,
):
    rollbots = await get_documents(collection_name)
    if rollbots:
        return ResponseModel(rollbots, "Rollbots successfulyl retrieved from db")
    return ResponseModel(rollbots, "Empty list returned")


@rollbots.get("/rollbot/{name}")
async def get_rollbot_by_name(name, collection_name: str = collection_name):
    rollbot = await get_document_by_name(collection_name, name)
    if rollbot:
        return ResponseModel(
            rollbot, "Successfully retrived Rollbot {} from DB".format(name)
        )
    return ErrorResponseModel("Error", 404, "Something went wrong retrieved from db")


@rollbots.post("/rollbot/")
async def add_rollbot_data(
    collection_name: str = collection_name, rollbot: RollbotSchema = Body(...)
):
    rollbot = jsonable_encoder(rollbot)
    new_rollbot = await create_document(collection_name, rollbot)
    print(new_rollbot)
    return ResponseModel(new_rollbot, "Rollbot added succesfully")
