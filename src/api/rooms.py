from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep
from src.exceptions import (
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get("")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-12-21"),
    date_to: date = Query(example="2025-12-28"),
):
    return await RoomService(db).get_rooms_by_time(hotel_id, date_from, date_to)


@router.post("", status_code=201)
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(),
):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException as exc:
        raise HTTPException(404, exc.detail)
    return {"status": "OK", "data": room}


@router.get("/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id=hotel_id, room_id=room_id)
    except (HotelNotFoundException, RoomNotFoundException) as exc:
        raise HTTPException(404, exc.detail)


@router.put("/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        await RoomService(db).edit_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except (HotelNotFoundException, RoomNotFoundException) as exc:
        raise HTTPException(404, exc.detail)
    return {"status": "OK"}


@router.patch("/{room_id}")
async def partial_edit_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    try:
        await RoomService(db).partial_edit_room(
            hotel_id=hotel_id, room_id=room_id, room_data=room_data
        )
    except (HotelNotFoundException, RoomNotFoundException) as exc:
        raise HTTPException(404, exc.detail)
    return {"status": "OK"}


@router.delete("/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except (HotelNotFoundException, RoomNotFoundException) as exc:
        raise HTTPException(404, exc.detail)
    return {"status": "OK"}
