import uuid

from django.db import models
from django.contrib.auth.models import User, Group

from Users.models import Profile


# Create your models here.
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
    parent_task = models.ForeignKey(  # for subtasks to store Task pk
        'self',
        on_delete=models.CASCADE,
        related_name='parent_task_fk',
        null=True,
        blank=True
    )
    sub_tasks = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='sub_tasks_fk'
    )
    executors = models.ManyToManyField(Profile, related_name='executors')

    def check_lists(self):
        if hasattr(self, 'checklist_set'):
            related_checklists = getattr(self, 'checklist_set')
            return related_checklists.all()
        raise NotImplementedError('No attr for related checklists found')

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

    def check_items(self):
        if hasattr(self, 'checklistitem_set'):
            checklist_items = getattr(self, 'checklistitem_set')
            return checklist_items.all()
        raise NotImplementedError('No attr for related check items')


    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<CheckList {self.uuid}>'
