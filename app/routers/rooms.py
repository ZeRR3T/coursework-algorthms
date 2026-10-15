from fastapi import APIRouter, Depends
from app.schemas import RoomCreate, RoomResponse
from app.dependencies import get_service
from app.service import HotelService

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])

@router.post("/", response_model=dict)
def create_room(room: RoomCreate, service: HotelService = Depends(get_service)):
    return service.add_room(room)

@router.get("/search/", response_model=list[RoomResponse])
def search_rooms(equipment: str, service: HotelService = Depends(get_service)):
    return service.find_rooms_by_equipment(equipment)

@router.get("/visualize/avl")
def visualize_avl(service: HotelService = Depends(get_service)):
    return service.get_avl_visualization_data()