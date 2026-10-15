from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Guest:
    passport: str
    full_name: str
    birth_year: int
    address: str
    arrival_purpose: str

@dataclass
class Room:
    number: str
    bed_count: int
    room_count: int
    has_bathroom: bool
    equipment: str

@dataclass
class StayRecord:
    passport: str
    room_number: str
    check_in_date: str
    check_out_date: str

    @property
    def is_active(self) -> bool:
        return not (self.check_out_date or "").strip()