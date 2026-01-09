from pydantic import BaseModel, EmailStr, Field


class UserRequestAdd(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    hashed_password: str


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)

    # model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
