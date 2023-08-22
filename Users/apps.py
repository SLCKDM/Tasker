from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Users'
    def ready(self):
        # import your signal file in here if the app is ready
        from . import signal