from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models_db import GuestDB, RoomDB, StayDB
from app.schemas import GuestCreate, RoomCreate, StayCreate
from app.algorithms.hash_table import HashTableOpen
from app.algorithms.avl_tree import AVLTree
from app.algorithms.cyclic_list import CyclicStayList
from app.algorithms.models import Guest, Room, StayRecord
from dataclasses import replace

class HotelService:
    def __init__(self):
        self.guests = HashTableOpen(capacity=17)
        self.rooms = AVLTree()
        self.stays = CyclicStayList()
        self._load_from_db()

    def _load_from_db(self):
        db = SessionLocal()
        try:
            for g in db.query(GuestDB).all():
                self.guests.put(g.passport, Guest(
                    passport=g.passport, full_name=g.full_name, 
                    birth_year=g.birth_year, address=g.address, 
                    arrival_purpose=g.arrival_purpose
                ))
            for r in db.query(RoomDB).all():
                self.rooms.insert(r.number, Room(
                    number=r.number, bed_count=r.bed_count, 
                    room_count=r.room_count, has_bathroom=r.has_bathroom, 
                    equipment=r.equipment
                ))
            for s in db.query(StayDB).all():
                self.stays.append(StayRecord(
                    passport=s.passport, room_number=s.room_number,
                    check_in_date=s.check_in_date, check_out_date=s.check_out_date
                ))
        finally:
            db.close()

    def add_guest(self, guest: GuestCreate):
        if self.guests.get(guest.passport):
            raise HTTPException(status_code=400, detail="Постоялец уже зарегистрирован")
        
        db = SessionLocal()
        try:
            db_guest = GuestDB(**guest.model_dump())
            db.add(db_guest)
            db.commit()
            self.guests.put(guest.passport, Guest(**guest.model_dump()))
            return {"message": "Постоялец зарегистрирован"}
        finally:
            db.close()

    def find_guest(self, passport: str):
        g = self.guests.get(passport)
        if not g:
            raise HTTPException(status_code=404, detail="Постоялец не найден")
        return g

    def add_room(self, room: RoomCreate):
        if self.rooms.find(room.number):
            raise HTTPException(status_code=400, detail="Номер уже существует")
            
        db = SessionLocal()
        try:
            db_room = RoomDB(**room.model_dump())
            db.add(db_room)
            db.commit()
            self.rooms.insert(room.number, Room(**room.model_dump()))
            return {"message": "Номер добавлен"}
        finally:
            db.close()

    def find_rooms_by_equipment(self, fragment: str):
        return self.rooms.find_by_equipment_fragment(fragment)

    def check_in(self, stay: StayCreate):
        if not self.guests.get(stay.passport):
            raise HTTPException(status_code=404, detail="Гость не найден")
        room = self.rooms.find(stay.room_number)
        if not room:
            raise HTTPException(status_code=404, detail="Номер не найден")
            
        used = sum(1 for r in self.stays.iter_records() if r.room_number == stay.room_number and r.is_active)
        if used >= room.bed_count:
            raise HTTPException(status_code=400, detail="Нет свободных мест")

        db = SessionLocal()
        try:
            db_stay = StayDB(**stay.model_dump())
            db.add(db_stay)
            db.commit()
            self.stays.append(StayRecord(**stay.model_dump()))
            return {"message": "Заселение зарегистрировано"}
        finally:
            db.close()

    def get_avl_visualization_data(self) -> dict:
        pos, edges = self.rooms.build_layout()
        return {
            "nodes": [{"id": k, "x": v[0], "y": v[1]} for k, v in pos.items()],
            "edges": [{"from": p, "to": c} for p, c in edges]
        }