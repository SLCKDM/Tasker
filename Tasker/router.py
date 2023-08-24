from django.urls import path,include
import TasksApp.router
import Users.router

app_name = 'api'
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('tasks/', include(TasksApp.router.router.urls)),
    path('users/', include(Users.router.router.urls)),
]