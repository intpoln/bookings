from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_instance = Celery("tasks", broker=settings.REDIS_URL, include=["src.tasks.tasks"])

celery_instance.conf.beat_schedule = {
    "checkin_nofity": {
        "task": "booking_today_checkin",
        "schedule": crontab(hour=8),
    }
}

# BASH:
#  celery --app src.tasks.celery_app:celery_instance worker --pool=solo -l INFO
#  celery -A src.tasks.celery_app:celery_instance beat -l INFO
