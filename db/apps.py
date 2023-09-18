from django.apps import AppConfig
# from suit.apps import DjangoSuitConfig


class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'


# class SuitConfig(DjangoSuitConfig):
    # layout = 'horizontal'