from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.api.docs_examples import hotel_post_doc_example
from src.exceptions import (
    HotelNotFoundException,
    ObjectNotFoundException,
)
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2025-12-21"),
    date_to: date = Query(example="2025-12-28"),
):
    return await HotelService(db).get_hotels(
        pagination=pagination,
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
    )


@router.post("", status_code=201)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples=hotel_post_doc_example),
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundException


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить location, а можно title</h1>",
)
async def partial_edit_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).partial_edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id=hotel_id)
    return {"status": "OK"}
