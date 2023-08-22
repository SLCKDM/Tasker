
from django.urls import path, include
from rest_framework import routers
from . import views


# profiles_list = views.ProfileViewSet.as_view({'get': 'list'})
# profiles_detail = views.ProfileViewSet.as_view({'get': 'retrieve'})

# urlpatterns = format_suffix_patterns([
#     path('', profiles_list, name='profile-list'),
#     path('<str:pk>', profiles_detail, name='profile-detail'),
# ])

router = routers.DefaultRouter()
router.register('profiles', views.ProfileViewSet, 'profile')

urlpatterns = [
    path('', include(router.urls)),
]