"""
URL configuration for Tasker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from rest_framework.schemas import get_schema_view

schema_url_patterns = [
    path('api/', include('Tasker.router'))
]

schema_view = get_schema_view(
    title='Tasker',
    description='Some task-managment project API',
    version='0.0.0.0.0.1',
    patterns=schema_url_patterns,
)

app_name = 'Tasker'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path("api/", include("Tasker.router")),
    path('openapi', schema_view, name='openapi-schema'),
    path("admin/", admin.site.urls),
    path('tasks/', include('TasksApp.urls')),
    path('profile/', include('Users.urls')),
]

urlpatterns