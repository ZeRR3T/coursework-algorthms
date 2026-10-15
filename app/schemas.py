from pydantic import BaseModel, Field, field_validator
import re

class GuestCreate(BaseModel):
    passport: str
    full_name: str = Field(..., min_length=1)
    birth_year: int = Field(..., gt=1900, lt=2100)
    address: str = Field(..., min_length=1)
    arrival_purpose: str = Field(..., min_length=1)

    @field_validator("passport")
    @classmethod
    def validate_passport(cls, v: str) -> str:
        if not re.match(r"^\d{4}-\d{6}$", v):
            raise ValueError("Формат паспорта: NNNN-NNNNNN (10 цифр с дефисом)")
        return v

class GuestResponse(GuestCreate):
    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    number: str
    bed_count: int = Field(..., gt=0)
    room_count: int = Field(..., gt=0)
    has_bathroom: bool
    equipment: str = Field(..., min_length=1)

    @field_validator("number")
    @classmethod
    def validate_room(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^[ЛПОМ]\d{3}$", v, re.IGNORECASE):
            raise ValueError("Формат: Л/П/О/М + 3 цифры (например О101)")
        return v[0].upper() + v[1:]

class RoomResponse(RoomCreate):
    class Config:
        from_attributes = True

class StayCreate(BaseModel):
    passport: str
    room_number: str
    check_in_date: str = Field(..., min_length=1)
    check_out_date: str = ""

class StayResponse(StayCreate):
    class Config:
        from_attributes = True