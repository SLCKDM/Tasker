from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

app_name = 'TasksApp'
urlpatterns = [
    path('', login_required(views.Index.as_view()), name='index'),
    path('<str:pk>/detail', login_required(views.TaskDetail.as_view()), name='detail'),
]
