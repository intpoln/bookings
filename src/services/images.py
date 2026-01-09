import shutil

from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    async def upload_image(self, file: UploadFile):
        base_path = f"src/static/images/{file.filename}"
        with open(base_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image.delay(base_path)


#  Сервис сделано некорректно, привязка к FastAPI. Лучше сделать свой интерфейс для работы с файлами
