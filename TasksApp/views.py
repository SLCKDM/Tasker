from os import pread
from typing import Any

from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from . import serializers
from . import models


# Django views

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

# DRF views

class TaskViewSet(viewsets.ModelViewSet,):
    lookup_field = "uuid"
    queryset = (models.Task.objects
                .select_related('author__user')
                .prefetch_related('child_tasks', 'parent_task', 'check_lists', 'executors')
                .all())
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class CheckListItemViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = models.CheckListItem.objects.prefetch_related('check_list').all()
    serializer_class = serializers.CheckListItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class CheckListViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = (models.CheckList.objects
                .prefetch_related('check_items')
                .select_related('task')
                .all())
    serializer_class = serializers.CheckListSerializer
    permission_classes = [permissions.IsAuthenticated]
