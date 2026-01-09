from pydantic import EmailStr
from sqlalchemy import or_, select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper, UserWithHashDataMapper


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def user_exists(self, email, username) -> dict:
        query = select(self.model).where(
            or_(self.model.email == email, self.model.username == username)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return UserWithHashDataMapper.map_to_domain_entity(model)
