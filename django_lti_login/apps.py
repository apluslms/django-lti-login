from django.apps import AppConfig
from django_settingsdict import SettingsDict

from . import BASE_CHARACTERS, SECRET_LENGTH


class DjangoLTILoginConfig(AppConfig):
    name = 'django_lti_login'
    verbose_name = 'Django LTI Login'

    def ready(self):
        from . import receivers  # NOQA


app_settings = SettingsDict(
    'AUTH_LTI_LOGIN',
    defaults={
        # At least one of the roles listed in this needs to be in login
        # for login to be accepted or None to accept any role.
        'ACCEPTED_ROLES': None,
        # Login with any of these roles will be marked as staff.
        'STAFF_ROLES': None,
        # Should we set session language from LTI params?
        'SET_LANGUAGE': True,
        # Do we create new object for unknown users?
        'CREATE_UNKNOWN_USER': True,
        # Extra tunables
        'KEY_CHARACTERS': BASE_CHARACTERS,
        'KEY_LENGTH': 16,
        'SECRET_CHARACTERS': BASE_CHARACTERS,
        'SECRET_LENGTH': 64,
    },
)
