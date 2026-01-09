from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, RoomNotFoundException
from src.schemas.bookings import BookingRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router.post("", status_code=201)
async def create_booking(booking_data: BookingRequest, db: DBDep, user_id: UserIdDep):
    try:
        booking = await BookingService(db).create_booking(booking_data, user_id)
    except AllRoomsAreBookedException as exc:
        raise HTTPException(409, exc.detail)
    except RoomNotFoundException as exc:
        raise HTTPException(404, exc.detail)
    return {"status": "OK", "data": booking}


@router.get("/me")
async def get_bookings_by_user(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_bookings_by_user(user_id)
