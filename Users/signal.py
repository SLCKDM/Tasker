from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from . import models

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)