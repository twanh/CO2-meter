import time

from celery.utils.log import get_task_logger
from .__main__ import celery

logger = get_task_logger(__name__)

@celery.task
def do_something(x, y):
    logger.info("GOT REQUEST")
    time.sleep(3)
    logger.info("DONE!")
    return x + y
