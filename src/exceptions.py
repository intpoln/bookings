from datetime import date

from fastapi import HTTPException


class BookingsException(Exception):
    detail = "Неизвестная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class ObjectNotFoundException(BookingsException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BookingsException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(BookingsException):
    detail = "Похожий объект уже существует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(422, "Дата заезда не может быть позже даты выезда")


class BookingHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundException(BookingHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundException(BookingHTTPException):
    status_code = 404
    detail = "Номер не найден"


#  Делаем обычные Exception - рейзим их в Services, делаем аналогичные HTTPExceptions - их в API ручки.
