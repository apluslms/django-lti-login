from django.apps import AppConfig


class ExampleAppConfig(AppConfig):
    name = 'exampleapp'
    verbose_name = 'ExampleApp'

    def ready(self):
        # Load our receivers
        # This is important as receiver hooks are not connected otherwise.
        from . import receivers  # NOQA
