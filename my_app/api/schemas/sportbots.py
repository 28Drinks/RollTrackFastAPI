from typing import Optional
from pydantic import BaseModel, Field


class StatsSchema(BaseModel):
    sportshares: int = Field(None)
    freebet: int = Field(None)
    comboboost: int = Field(None)


class TraitsSchema(BaseModel):
    sport: str = Field(None)
    background: str = Field(None)
    body: str = Field(None)
    eyes: str = Field(None)
    teeth: str = Field(None)


class SportbotSchema(BaseModel):
    name: str
    number: int
    image_url: str
    revealed: bool
    stats: Optional[StatsSchema] = None
    traits: Optional[TraitsSchema] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Sportbot#28",
                "number": 28,
                "image_url": "https://somerandomurl.2523525",
                "revealed": True,
                "stats": {"sportshares": 10, "freebet": 28, "comboboost": 103},
                "traits": {"sport": "Boxing", "background": "purple", "body": "gold", "eyes": "rusty-eyes", "teeth": "rusty-mouth"}
            }
        }


class UpdateSportBotSchema(BaseModel):
    name: Optional[str]
    number: Optional[int]
    image_url: Optional[str]
    revealed: Optional[bool]
    stats: Optional[StatsSchema]
    traits: Optional[TraitsSchema]