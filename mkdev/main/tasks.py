from celery import shared_task
from celery.utils.log import get_task_logger

from mkdev.celery import app

from .email import send_email_task
from .runapscheduler import products_of_the_week

logger = get_task_logger(__name__)


@app.task(name='send_email_task_product')
def send_email_task_product(title,slug, description, price):
    logger.info("Sent a mesasge")
    return send_email_task(title,slug, description, price)


@shared_task
def week_email_product():
    logger.info("Sent a mesasge")
    return products_of_the_week

