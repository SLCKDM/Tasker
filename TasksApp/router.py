from django.urls import path, include
from rest_framework import routers

from . import views

class OptionalSlashDefaultRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

router = OptionalSlashDefaultRouter()
router.register('tasks', views.TaskViewSet, 'tasks')
router.register('checkitems', views.CheckListItemViewSet, 'checkitems')
router.register('checklists', views.CheckListViewSet, 'checklists')
