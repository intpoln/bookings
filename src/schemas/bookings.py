from datetime import date

from pydantic import BaseModel


class BookingRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BaseModel):
    user_id: int
    price: int
    date_from: date
    date_to: date
    room_id: int


class Booking(BookingAdd):
    id: int

    # model_config = ConfigDict(from_attributes=True)


class BookingPatchRequest(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None
    room_id: int | None = None
