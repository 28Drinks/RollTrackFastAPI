from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime, timedelta
from bson import ObjectId

from .sportbots import SportbotSchema, UpdateSportBotSchema


class BotClaims(BaseModel):
    claimed_at: datetime | None = None
    claimed_share: float | None = None
    claimed_freebet: int | None = None
    claimed_freebet_result: bool | None = None
    claimed_freebet_multi: float | None = None


class BotInInventory(BaseModel):
    bot_id: str
    claimed: bool | None = None
    last_claimed_at: datetime | None = None
    total_claims: int | None = None
    claims: List[BotClaims] | None = None
    value: float | None = None
    buy_price: float | None = None

    
class UserIventorySchema(BaseModel):
    user_id: str
    bots: List[BotInInventory]


class AddInventoryEntrySchema(BotInInventory):
    pass

class UpdateBot(BotInInventory):
    claimed: bool | None = None
    last_claimed_at: datetime | None = None
    total_claims: int | None = None
    value: float | None = None
    buy_price: float | None = None