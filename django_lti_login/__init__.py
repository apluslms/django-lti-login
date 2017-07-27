import string


BASE_CHARACTERS = string.ascii_letters + string.digits
SAFE_CHARACTERS = frozenset(BASE_CHARACTERS + '-')
KEY_LENGTH = (6, 128)
NONCE_LENGTH = (6, 128)
SECRET_LENGTH = (6, 128)


default_app_config = 'django_lti_login.apps.DjangoLTILoginConfig'
