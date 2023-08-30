from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from . import models

User = get_user_model()
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)

# @receiver(post_save)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)