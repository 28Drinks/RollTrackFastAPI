from datetime import datetime, timedelta
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder


from schemas.share import *
from schemas.util import *

share = APIRouter()

collection_name = "share"

# Share


@share.get("/share/")
async def get_share_data(collection_name: str = collection_name):
    share = get_documents(collection_name)
    if share:
        return ResponseModel(share, "Success")
    return ErrorResponseModel("Error", 404, "something wrong")


#
