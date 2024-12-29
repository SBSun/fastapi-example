from celery import Celery

from config import get_settings
from user.application.send_welcome_email_task import SendWelcomeEmailTask

settings = get_settings()

celery = Celery(
    "fastapi-ca",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
    # 워커가 수행될 때 브로커와의 연결이 제대로 이루어지지 않으면 연결을 반복적으로 시도할지에 대한 설정
    broker_connection_retry_on_startup=True
)

celery.register_task(SendWelcomeEmailTask())