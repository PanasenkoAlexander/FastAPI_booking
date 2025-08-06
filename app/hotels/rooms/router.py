from datetime import date, datetime, timedelta
from typing import List

from fastapi import Query

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.router import router


# @router.get("/{hotel_id}/rooms")
# async def get_rooms(user: Users = Depends(get_current_user)) -> list[SBooking]:
#     return await BookingDAO().find_all(user_id=user.id)


# !!! нужно разобраться с этой ручкой !!!
# @router.get("/{hotels}/rooms")
# async def get_rooms_by_time(
#         hotel_id: int,
#         date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
#         date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
# ) -> list[SRoomInfo]:
#     rooms = await HotelDAO().search_for_rooms(hotel_id, date_from, date_to)
#     return rooms


@router.get("/{hotel_id}/rooms")
# Этот эндпоинт можно и нужно кэшировать, но в курсе этого не сделано, чтобы
# можно было проследить разницу в работе /rooms (без кэша) и /hotels (с кэшем).
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SRoomInfo]:
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    return rooms
