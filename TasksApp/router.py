from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tasks', views.TaskViewSet, 'tasks')
router.register('checkitems', views.CheckListItemViewSet, 'checkitems')
router.register('checklists', views.CheckListViewSet, 'checklists')

urlpatterns = [path('tasks/', include(router.urls))]
