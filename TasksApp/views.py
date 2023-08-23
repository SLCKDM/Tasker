from typing import Any

from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets
from rest_framework import permissions

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

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class CheckListItemViewSet(viewsets.ModelViewSet):
    queryset = models.CheckListItem.objects.all()
    serializer_class = serializers.CheckListItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class CheckListViewSet(viewsets.ModelViewSet):

    queryset = models.CheckList.objects.all()
    serializer_class = serializers.CheckListSerializer
    permission_classes = [permissions.IsAuthenticated]