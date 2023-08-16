from django.urls import path, include
from . import views

app_name = 'TasksApp'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<str:pk>/detail', views.TaskDetail.as_view(), name='detail'),
]
