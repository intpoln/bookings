import asyncio
import logging
import os

from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def resize_image(image_path: str):
    logging.info('Вызывается фоновая задача Celery: "ResizeImage"')
    sizes = [640, 480, 240]
    output_folder = "src/static/images"

    img = Image.open(image_path)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    print(f"Начал ресайзить {image_path}")

    for size in sizes:
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.NEAREST
        )

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)

        img_resized.save(output_path)

    logging.info(f"Изображение сохранено в размерах: {sizes} в папке {output_folder}")

    try:
        os.remove(image_path)
        logging.info(f"Исходное изображение {base_name} удалено")
    except FileNotFoundError as e:
        logging.info(f"Ошибка при удалении файла: {e}")
        raise


async def get_bookings_with_today_checkin_helper():
    logging.info("Вызывается фоновая задача Celery: 'get_bookings_with_today_checkin_helper'")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin
        logging.info(f"Фоновая задача завершилась: {bookings=}")


@celery_instance.task(name="booking_today_checkin")
def notify_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
