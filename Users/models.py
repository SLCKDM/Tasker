import uuid

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.query import QuerySet


# Managers

class ProfileManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def create(
        self, user: dict, f_name: None | str = None, l_name: None | str = None,
        group: None | dict = None
    ) -> 'Profile':
        new_profile = Profile(f_name=f_name, l_name=l_name, group=group, user=user)
        new_profile.save()
        return new_profile

# Models


class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100, blank=True, null=True)
    l_name = models.CharField(max_length=100, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    # objects = ProfileManager()

    def username(self):
        return self.user.username

    def __repr__(self):
        return f'<Profile {self.uuid}>'

    def __str__(self) -> str:
        return f'{self.user.username}'
