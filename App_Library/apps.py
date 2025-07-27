from django.apps import AppConfig


class AppLibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_Library'

    def ready(self):
        import App_Library.signals

