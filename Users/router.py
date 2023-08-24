from django.urls import path, include
from rest_framework import routers

from . import views

class OptionalSlashDefaultRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

router = OptionalSlashDefaultRouter()
router.register('profiles', views.ProfileViewSet, 'profiles')
