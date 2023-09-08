from typing import Iterable
from celery import shared_task
import logging
from . import models

@shared_task
def notify_done_task(task_id: str, executors_ids: Iterable[str]):
    for executor in executors_ids:
        logging.info('<%s> DONE TASK %s' % (executor, task_id))
