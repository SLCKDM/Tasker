from typing import Any, Optional
from django.db import models
from django.shortcuts import render
from django.views import generic

from . import models

class ProfileDetail(generic.DetailView):
    template_name = 'Users/detail.html'
    model = models.Profile

