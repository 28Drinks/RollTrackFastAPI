
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class SportEntrySchema(BaseModel):
    share_value: float
    date_time: datetime


class ShareSchema(BaseModel):
    sport: str 
    total_shares: int
    total_bots: int
    base_value: float
    total_value: float
    share_entrys: List[SportEntrySchema]


class UpdateShareSchema(BaseModel):
    sport: Optional[str]
    total_shares: Optional[int]
    total_bots: Optional[int]
    base_value: Optional[float]
    total_value: Optional[float]
    share_entrys: Optional[List[SportEntrySchema]]


class ReadShareSchema(ShareSchema):
    pass

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "sport": "Soccer",
    #             "total_shares": 1255,
    #             "total_bots": 333,
    #             "base_value": 7.69,
    #             "total_value": 28125.04,
    #             "share_entrys":  [
    #                     {"share_value": 5.28, "date_time": "2023-03-01T00:00:00"},
    #                     {"share_value": 14.78, "date_time": "2023-03-02T00:00:00"},
    #                     {"share_value": 3.32, "date_time": "2023-03-03T00:00:00"},
    #                 ]
    #         }
    #     }



