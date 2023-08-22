from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'Users'
urlpatterns = [
    path('<str:pk>', login_required(views.ProfileDetail.as_view()), name='detail'),
]