from django.apps import AppConfig


class AdvertisementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advertisement'



class YourAppConfig(AppConfig):
    name = 'advertisement'

    def ready(self):
        from . import signals

