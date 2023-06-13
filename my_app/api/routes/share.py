from datetime import datetime, timedelta
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from typing import Optional

from schemas.share import *
from schemas.util import *

from CRUD.share import *

share = APIRouter()

@share.get("/share/")
async def get_share_data(sport: Optional[str] = None, date: Optional[str] = None, limit: Optional[int] = None):
    share = await get_all_share(sport, date, limit)
    if share:
        return share
    return ErrorResponseModel("Error", 404, "something wrong")