from django.views import generic
from rest_framework import viewsets
from rest_framework import permissions

from . import models
from . import serializers

# Vanilla Django views

class ProfileDetail(generic.DetailView):
    lookup_field = 'uuid'
    template_name = 'Users/detail.html'
    model = models.Profile

# # DRF views
# class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
#     '''
#     EP that allows profiles to be viewed or editred.
#     '''
#     lookup_field = 'uuid'
#     queryset = models.Profile.objects.all()
#     serializer_class = serializers.ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    model = models.Profile
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    lookup_field = 'uuid'
    permission_classes = [permissions.IsAuthenticated]
