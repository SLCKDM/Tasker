from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from . import models

class Index(generic.ListView):
    model = models.Task
    template_name = 'TasksApp/index.html'
    context_object_name = 'tasks'


class TaskDetail(generic.DetailView):
    model = models.Task
    template_name = 'TasksApp/detail.html'
    context_object_name = 'task'

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs['pk'])