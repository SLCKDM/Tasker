import uuid

from django.db import models
from django.contrib.auth.models import User, Group


class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True,
                              blank=True)

    def username(self):
        return self.user.username

    def __repr__(self):
        return f'<Profile {self.uuid}>'

    def __str__(self) -> str:
        return f'{self.user.username}'
