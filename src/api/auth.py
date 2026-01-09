from fastapi import APIRouter, Body, HTTPException, Request, Response
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from src.api.dependencies import DBDep, UserIdDep
from src.api.docs_examples import user_login_example, user_register_example
from src.exceptions import ObjectAlreadyExistsException
from src.schemas.users import UserAdd, UserLogin, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login", status_code=201)
async def login_user(
    response: Response,
    db: DBDep,
    data: UserLogin = Body(openapi_examples=user_login_example),
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(401, detail="Пароль неверный")

    access_token = AuthService().create_access_token({"user_id": user.id})
    refresh_token = AuthService().create_refresh_token({"user_id": user.id})

    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh_tokens(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token отсутствует")

    try:
        data = AuthService().decode_token(refresh_token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token истёк")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Невалидный refresh token")

    if data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Невалидный тип токена")

    user_id = data.get("user_id")
    access_token = AuthService().create_access_token({"user_id": user_id})
    new_refresh_token = AuthService().create_refresh_token({"user_id": user_id})

    response.set_cookie("access_token", access_token)
    response.set_cookie("refresh_token", new_refresh_token, httponly=True)

    return {"access_token": access_token, "refresh_token": new_refresh_token}


@router.post("/register", status_code=201)
async def register_user(
    db: DBDep,
    data: UserRequestAdd = Body(openapi_examples=user_register_example),
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name,
    )
    try:
        await db.users.add(new_user_data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(409, "Пользователь с такими данными уже существует")

    return {"status": "OK"}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await db.users.get_one_or_none(id=user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Вы успешно вышли из системы"}
