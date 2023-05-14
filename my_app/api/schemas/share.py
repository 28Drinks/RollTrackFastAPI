
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
    share_entrys: List[SportEntrySchema]


class UpdateShareSchema(BaseModel):
    sport: Optional[str]
    total_shares: Optional[int]
    total_bots: Optional[int]
    share_entrys: Optional[List[SportEntrySchema]]


class ReadShareSchema(ShareSchema):
    pass


