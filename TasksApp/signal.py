from django.dispatch import receiver
from django.db.models.signals import (post_save,)

from . import models
from . import tasks


@receiver(post_save, sender=models.Task)
def update_parent_task(sender, instance: models.Task, created, **kwargs):
    task = instance
    if task.done:
        tasks.notify_done_task.delay(
            task_id=str(task.uuid),
            executors_ids=[executor.uuid for executor in task.executors.all()]
        )