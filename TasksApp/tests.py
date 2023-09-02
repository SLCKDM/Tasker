# from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from .models import Task
from Users.models import Profile

def get_user(username: str) -> Profile:
    User.objects.create(username='root', password='root')
    user = User.objects.get(username='root')
    profile: Profile = getattr(user, 'profile')
    return profile


class TaskTests(APITestCase):


    def test_create(self):
        profile = get_user('test_user')
        self.client.force_login(profile.user)
        url = reverse('api:tasks-list')
        data = {
            'title': 'TEST',
            'description': 'TEST DESC',
            'author': reverse('api:profiles-detail', [profile.uuid])
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_ident = response.json()['uuid']
        task = Task.objects.get(uuid=task_ident)
        self.assertEqual(task.title, response.json()['title'])

class CheckListsTests(APITestCase):

    def test_create(self):
        ...

    def create_with_checkitems():
        ...