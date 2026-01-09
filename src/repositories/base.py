import logging
from typing import Sequence

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            # print(add_data_stmt.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as exc:
            logging.error(
                f"Не удалось добавить данные в БД."
                f"Входные данные: {data}"
                f"Тип ошибки: {type(exc.orig.__cause__)=}"
            )
            if isinstance(exc.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from exc
            else:
                logging.error(f"Неизвестная ошибка: {type(exc.orig.__cause__)=}")
                raise exc

    async def add_bulk(self, data: Sequence[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        # print(add_data_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        # print(update_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        # print(delete_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_stmt)
