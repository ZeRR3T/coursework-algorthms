import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import Base, engine
from app.routers import guests, rooms, stays
from app.service import HotelService

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Настройка путей для шаблонов
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация структур при запуске
    app.state.service = HotelService()
    print("Структуры данных (Hash, AVL, List) загружены в память.")
    yield
    print("Завершение работы.")

app = FastAPI(
    title="Курсовой проект: Гостиница (Алгоритмы + FastAPI)",
    lifespan=lifespan
)

app.include_router(guests.router)
app.include_router(rooms.router)
app.include_router(stays.router)

# Маршрут для отдачи HTML странички
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")