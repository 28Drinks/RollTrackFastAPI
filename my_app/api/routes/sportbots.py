from datetime import datetime, timedelta
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from json import JSONDecodeError

from schemas.sportbots import *
from schemas.util import *

from CRUD.sportbots import *

sportbots = APIRouter()


@sportbots.get("/sportbots/{number}")
async def get_bot_by_number(number: int):
    sportbot = await get_sportbot_by_number(number)
    if sportbot:
        return sportbot, "Successfully retrived Sportbot {} from DB".format(number)
    return ErrorResponseModel("Error", 404, "Something went wrong retrieved from db")
