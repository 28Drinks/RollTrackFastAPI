
from typing import Optional
from pydantic import BaseModel, Field


class StatsSchema(BaseModel):
    rollback: float
    revshare: float
    marketStakes: int
    lotteryStakes: int
    lotteryMultiplier: float


class TraitsSchema(BaseModel):
    background: str
    body: str
    clothes: str
    ears: str
    eyes: str
    hat: str
    teeth: str


class RollbotSchema(BaseModel):
    name: str = Field(...)
    number: int = Field(...)
    image_url: str = Field(...)
    stats: StatsSchema = Field(...)
    traits: TraitsSchema = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Rollbot#28",
                "number": 28,
                "image_url": "https://randomurlofimage.42453",
                "stats": {"rollback": 5.5, "revshare": 28, "marketStakes": 100000, "lotteryStakes": 150000, "lotteryMultiplier": 4.4},
                "traits": {"background": "Black", "body": "steel", "clothes": "carpet", "ears": "no-ears", "eyes": "777 eyes", "hat": "melone hat", "teeth": "gold teeth"}
            }
        }
