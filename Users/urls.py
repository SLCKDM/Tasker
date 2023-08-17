from django.urls import path
from . import views

app_name = 'Users'
urlpatterns = [
    path('<str:pk>', views.ProfileDetail.as_view(), name='detail'),
]