from django.apps import AppConfig


class DjangoAppApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app_api'

    # noinspection PyUnresolvedReferences
    def ready(self):
        import django_app_api.signals
