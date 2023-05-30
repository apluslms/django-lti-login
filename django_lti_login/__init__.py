import string


BASE_CHARACTERS = string.ascii_letters + string.digits
SAFE_CHARACTERS = frozenset(BASE_CHARACTERS + '-_.')
KEY_LENGTH = (2, 128)
NONCE_LENGTH = (6, 128)
SECRET_LENGTH = (6, 128)
