from datetime import datetime, timedelta
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from typing import Optional

from schemas.share import *
from schemas.util import *

from CRUD.share import *

share = APIRouter()

@share.get("/share/")
async def get_share_data(sport: Optional[str] = None, date: Optional[str] = None):
    share = await get_all_share(sport, date)
    if share:
        return share
    return ErrorResponseModel("Error", 404, "something wrong")


@share.get("/share/sport/")
async def get_share_data_by_sport(sport: str):
    share_sport = await get_share_by_sport(sport)
    if share_sport:
        return share_sport
    return ErrorResponseModel("Error", 404, "something wrong")


@share.get("/share/date/")
async def get_share_data_by_date(share_date: Optional[str] = None, hour: Optional[str] = None):
    if hour:
        share_date = share_date + " " + hour
    result = await get_share_by_day(share_date)
    if result:
        return result
    return ErrorResponseModel("Error", 404, "something wrong")
