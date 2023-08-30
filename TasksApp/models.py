from typing import Any, Iterable, MutableMapping, Optional, Sequence, Tuple
import uuid

import datetime as dt
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.query import QuerySet

from Users.models import Profile


# Managers

# class CheckListManager(models.Manager):

#     def create(self, **data):
#         new_check_items = data.pop('check_items')
#         new_checklist = CheckList(**data)
#         new_checklist.save()
#         for check_item in new_check_items:
#             CheckListItem(
#                 text=check_item.get('text', ''),
#                 done=check_item.get('done', False),
#                 check_list=new_checklist
#             ).save()
#         return new_checklist


# class TaskManager(models.Manager):

#     def create(self, **data):
#         check_lists = data.pop('check_lists', None)
#         sub_tasks = data.pop('sub_tasks', None)
#         parent_task = data.pop('parent_task', None)
#         new_task = Task(**data)
#         new_task.save()
#         for check_list in check_lists:
#             check_list(task=new_task.uuid).save()
#         return new_task




# Models

class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    done = models.BooleanField(default=False)
    done_dt = models.DateTimeField(null=True, blank=True)
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL,
                                    related_name='child_tasks', null=True,
                                    blank=True)
    executors = models.ManyToManyField(Profile, related_name='related_tasks')

    def __repr__(self):
        return f'<Task {self.title}>'

    def __str__(self) -> str:
        return f'{self.title}'

    def save(self, *args, **kwargs) -> None:
        self.updated=dt.datetime.now()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['created', 'updated', 'deadline']


class CheckListItem(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    text = models.CharField(max_length=300)
    done = models.BooleanField(default=False)
    check_list = models.ForeignKey('CheckList', on_delete=models.CASCADE,
                                   related_name='check_items')

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'<CheckListItem {self.uuid}>'


class CheckList(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    name = models.CharField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='check_lists')


    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<CheckList {self.uuid}>'
