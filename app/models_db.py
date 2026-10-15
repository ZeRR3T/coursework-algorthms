from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class GuestDB(Base):
    __tablename__ = "guests"
    passport = Column(String, primary_key=True, index=True)
    full_name = Column(String, index=True)
    birth_year = Column(Integer)
    address = Column(String)
    arrival_purpose = Column(String)

class RoomDB(Base):
    __tablename__ = "rooms"
    number = Column(String, primary_key=True, index=True)
    bed_count = Column(Integer)
    room_count = Column(Integer)
    has_bathroom = Column(Boolean)
    equipment = Column(String)

class StayDB(Base):
    __tablename__ = "stays"
    id = Column(Integer, primary_key=True, autoincrement=True)
    passport = Column(String, index=True)
    room_number = Column(String, index=True)
    check_in_date = Column(String)
    check_out_date = Column(String, default="")