from celery.utils.log import get_task_logger

from mkdev.celery import app

from .email import send_email_task

logger = get_task_logger(__name__)


@app.task(name='send_email_task')
def send_email_task_product(title,slug, description, price):
    logger.info("Sent a mesasge")
    return send_email_task(title,slug, description, price)




