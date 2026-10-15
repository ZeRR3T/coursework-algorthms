from fastapi import APIRouter, Depends
from app.schemas import StayCreate
from app.dependencies import get_service
from app.service import HotelService

router = APIRouter(prefix="/api/stays", tags=["Stays"])

@router.post("/check-in", response_model=dict)
def check_in_guest(stay: StayCreate, service: HotelService = Depends(get_service)):
    return service.check_in(stay)