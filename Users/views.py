from django.views import generic
from rest_framework import viewsets
from rest_framework import permissions

from . import models
from . import serializers

# Vanilla Django views

class ProfileDetail(generic.DetailView):
    template_name = 'Users/detail.html'
    model = models.Profile

# DRF views
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    EP that allows profiles to be viewed or editred.
    '''
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]