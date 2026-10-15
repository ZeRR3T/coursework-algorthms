from fastapi import APIRouter, Depends
from app.schemas import GuestCreate, GuestResponse
from app.dependencies import get_service
from app.service import HotelService

router = APIRouter(prefix="/api/guests", tags=["Guests"])

@router.post("/", response_model=dict)
def create_guest(guest: GuestCreate, service: HotelService = Depends(get_service)):
    return service.add_guest(guest)

@router.get("/{passport}", response_model=GuestResponse)
def get_guest(passport: str, service: HotelService = Depends(get_service)):
    return service.find_guest(passport)