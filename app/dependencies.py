from fastapi import Request
from app.service import HotelService

def get_service(request: Request) -> HotelService:
    return request.app.state.service