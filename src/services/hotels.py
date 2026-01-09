from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import (
    HotelNotFoundException,
    ObjectNotFoundException,
    check_date_to_after_date_from,
)
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination: PaginationDep,
        location: str | None = None,
        title: str | None = None,
        date_from: date = date.today(),
        date_to: date = date.today(),
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd) -> None:
        await self.db.hotels.edit(id=hotel_id, hotel_data=hotel_data)
        await self.db.commit()

    async def partial_edit_hotel(self, hotel_id: int, hotel_data: HotelPatch) -> None:
        await self.db.hotels.edit(id=hotel_id, hotel_data=hotel_data, exclude_unset=True)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int) -> None:
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def check_hotel_exists(self, hotel_id: int) -> None:
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as exc:
            raise HotelNotFoundException from exc
