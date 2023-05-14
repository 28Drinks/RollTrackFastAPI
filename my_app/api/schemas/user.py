from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime, timedelta
from bson import ObjectId


class UserSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    hashed_password: str
    created_at: datetime | None = None
    status: str | None = None
    disabled: bool | None = None
    inventory_id: str | None = None


class UpdateUserSchema(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    created_at: Optional[datetime]
    status: Optional[str]
    disabled: Optional[bool]
    inventory_id: Optional[str]
    

class ReadUserSchema(UpdateUserSchema):
    pass
