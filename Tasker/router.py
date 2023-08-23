from django.urls import path,include

app_name = 'API'
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include('TasksApp.router')),
    path('', include('Users.router')),
]