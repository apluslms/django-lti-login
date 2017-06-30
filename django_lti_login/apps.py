from django.apps import AppConfig
from django_settingsdict import SettingsDict

from . import BASE_CHARACTERS, SECRET_LENGTH


class DjangoLTILoginConfig(AppConfig):
    name = 'django_lti_login'
    verbose_name = 'Django LTI Login'


app_settings = SettingsDict(
    'LTI_LOGIN',
    defaults={
        'KEY_CHARACTERS': BASE_CHARACTERS,
        'KEY_LENGTH': 16,
        'SECRET_CHARACTERS': BASE_CHARACTERS,
        'SECRET_LENGTH': 64,
    },
)
