from django.dispatch import receiver
from django.db.models.signals import (post_save,)
from . import models


# @receiver(post_save, sender=models.Task)
# def update_parent_task(sender, instance, created, **kwargs):
#     instance.updated =