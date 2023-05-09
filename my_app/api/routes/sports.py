from datetime import datetime, timedelta
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from schemas.share import *
from schemas.util import *

from db_helper import (
    create_document,
    get_document_by_id,
    get_document_by_name,
    get_document_by_sport,
    get_documents,
    get_sport_by_sport,
    update_sport_by_sport,
    get_sport_shares,
    create_sport_share,
)

sports = APIRouter()

collection_name = "sports_collection"

# Sports


@sports.get("/sports/")
async def get_rollbots(collection_name: str = collection_name):
    sports = await get_documents(collection_name)
    if sports:
        return ResponseModel(sports, "Rollbots successfulyl retrieved from db")
    return ResponseModel(sports, "Empty list returned")


@sports.get("/sports/{sport}")
async def get_rollbot_by_name(sport, collection_name: str = collection_name):
    sport_data = await get_sport_by_sport(collection_name, sport)
    if sport_data:
        return ResponseModel(
            sport_data, "Successfully retrived Sport {} from DB".format(sport)
        )
    return ErrorResponseModel("Error", 404, "Something went wrong retrieved from db")


@sports.post("/sports/")
async def add_sport_data(
    collection_name: str = collection_name, sport: UpdateShareSchema = Body(...)
):
    sport_data = jsonable_encoder(sport)
    new_sport = await create_document(collection_name, sport_data)
    print(new_sport)
    return ResponseModel(new_sport, "Sport added succesfully")


@sports.put("/sports/{sport}")
async def update_sport_data(
    sport: str,
    collection_name: str = collection_name,
    update_data: UpdateShareSchema = Body(...),
):
    sport_ele = await get_sport_by_sport(collection_name, sport)
    if sport_ele is None:
        return {"Sport not found"}

    updated_sport_ele = await update_sport_by_sport(
        collection_name, sport_ele["sport"], update_data
    )
    if updated_sport_ele is None:
        return {"update failed"}

    return updated_sport_ele


# Sport Share Entrys


# GET
@sports.get("/sports/{sport}/shares")
async def get_sport_share(sport: str, collection_name: str = collection_name):
    sport_ele = await get_sport_by_sport(collection_name, sport)
    if sport_ele is None:
        return {"Sport not found"}

    get_shares = await get_sport_shares(collection_name, sport_ele["sport"])
    if get_shares is None:
        return {"update failed"}

    return get_shares


# POST
@sports.post("/sports/{sport}/shares")
async def post_sport_share(
    sport: str, share: SportEntrySchema, collection_name: str = collection_name
):
    share = jsonable_encoder(share)
    sport_ele = await get_sport_by_sport(collection_name, sport)
    if sport_ele is None:
        return {"Sport not found"}

    post_share = await create_sport_share(collection_name, sport_ele["sport"], share)
    if post_share is None:
        return {"Share post failed"}

    return sport_ele, post_share


# PUT
