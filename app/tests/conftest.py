import asyncio
import datetime
import json
import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users

from httpx import AsyncClient
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # убеждаемся, что работаем с тестовой БД
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        # Удаление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.drop_all)
        # Добавление всех заданных нами таблиц в БД
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model:str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    # преобразование формата времени для sqlalchemy
    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Hotels, hotels),
            (Rooms, rooms),
            (Users, users),
            (Bookings, bookings),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


# функция взята из документации
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# асинхронный клиент для тестирования эндпоинтов
@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


# асинхронный аутентифицированный клиент для тестирования эндпоинтов
@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("auth/login", json={
            "email": "test@test.com",
            "password": "test",
        })
        assert ac.cookies["booking_access_token"]
        yield ac
