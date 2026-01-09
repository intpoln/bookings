from src.exceptions import (
    AllRoomsAreBookedException,
    ObjectNotFoundException,
    RoomNotFoundException,
)
from src.schemas.bookings import BookingAdd, BookingRequest
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def create_booking(self, booking_data: BookingRequest, user_id: int):
        try:
            room: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc
        room_price: int = room.price
        _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
        try:
            booking = await self.db.bookings.add_booking(_booking_data)
        except AllRoomsAreBookedException as exc:
            raise exc
        await self.db.commit()
        return booking

    async def get_bookings_by_user(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)
