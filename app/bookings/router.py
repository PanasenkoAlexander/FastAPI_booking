from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic.v1 import parse_obj_as
from sqlalchemy import select
from app.database import async_session_maker
from app.bookings.models import Bookings
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingInfo
from app.exceptions import RoomCannotBeBookedException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from datetime import date

router = APIRouter(
    prefix="/bookings",
    tags=["Booking"]
)

# один вариант
# @router.get("")
# async def get_bookings():
#     async with async_session_maker() as session:
#         query = select(Bookings)
#         result = await session.execute(query)
#         return result.mappings().all()

# другой вариант
@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.find_all_with_images(user_id=user.id)
# async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
#     return await BookingDAO().find_all(user_id=user.id)

@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    # для удобства работы с Celery
    booking_dict = parse_obj_as(SBooking, booking).model_dump()
    # если используем Celery, то должен быть навешен декоратор @celery.task
    send_booking_confirmation_email.delay(booking_dict, user.email)
    # Background Tasks - встроено в FastAPI
    # background_tasks.add_task(send_booking_confirmation_email, booking, user.email)
    if not booking:
        raise RoomCannotBeBookedException
    return booking_dict


@router.delete("/{booking_id}")
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)

# @router.get("/{booking_id}")
# async def get_bookings() -> list[STask]:
#     tasks = await TaskRepository.find_all()
#     return tasks
