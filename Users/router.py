from django.urls import path
from rest_framework import routers
from . import views


# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet.as_view())
# router.register(r'groups')

urlpatterns = [
    path('', views.UsersListViewSet.as_view()),
    path('<str:pk>', views.UserView.as_view()),
]