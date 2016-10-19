from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'app'
    verbose_name = "Hero App"

    def ready(self):
        pass
