from datetime import date

from src.schemas.bookings import BookingAdd, BookingPatchRequest


async def test_booking_crud(db):
    #  CREATE
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    booking_data = BookingAdd(
        date_from=date(year=2025, month=9, day=1),
        date_to=date(year=2025, month=9, day=8),
        room_id=room_id,
        user_id=user_id,
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)
    await db.commit()

    #  READ
    booking_read = await db.bookings.get_one_or_none(id=new_booking.id)

    assert booking_read
    assert BookingAdd.model_dump(booking_read, exclude={"id"}) == booking_data.model_dump()

    #  UPDATE
    booking_patch_data = BookingPatchRequest(
        date_from=date(year=2014, month=3, day=5),
        date_to=date(year=2014, month=4, day=5),
        room_id=room_id,
        price=1000,
    )

    await db.bookings.edit(booking_patch_data, id=new_booking.id)
    await db.commit()

    booking_updated = await db.bookings.get_one_or_none(id=new_booking.id)

    assert booking_updated
    assert (
        BookingPatchRequest.model_dump(booking_updated, exclude={"id", "user_id"})
        == booking_patch_data.model_dump()
    )

    #  DELETE
    await db.bookings.delete(id=new_booking.id)
    await db.commit()

    booking_deleted = await db.bookings.get_one_or_none(id=new_booking.id)

    assert not booking_deleted
