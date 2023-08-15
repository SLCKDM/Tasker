from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group
import uuid

# Create your models here.

class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    group = models.OneToOneField(Group, on_delete=models.SET_NULL, null=True,
                                 blank=True)

    def username(self):
        return self.user.username

    def __repr__(self):
        return f'<Profile {self.uuid}>'

    def __str__(self) -> str:
        return f'{self.user.username}'


class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    done_dt = models.DateTimeField(null=True, blank=True)

    sub_tasks = models.ManyToManyField('Task', blank=True)
    executors = models.ManyToManyField(Profile, related_name='executors')

    def __repr__(self):
        return f'<Task {self.uuid}>'

    def __str__(self) -> str:
        return f'{self.title}'


class CheckListItem(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    text = models.CharField(max_length=300)
    done = models.BooleanField(default=False)

    check_list = models.ForeignKey('CheckList', on_delete=models.CASCADE)


    def __str__(self):
        return self.text

    def __repr__(self):
        return f'<CheckListItem {self.uuid}>'

class CheckList(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    name = models.CharField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<CheckList {self.uuid}>'
