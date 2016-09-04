from oauthlib.oauth1 import RequestValidator

from . import SAFE_CHARACTERS_SET, KEY_LENGTH
from .models import LTIClient

class LTIRequestValidator(RequestValidator):
    def __init__(self):
        self.__secrets = {}

    @property
    def safe_characters(self):
        """ Allow also '-' character used in some uuid examples out there. """
        return SAFE_CHARACTERS_SET

    @property
    def client_key_length(self):
        """ Loosen limits. """
        return KEY_LENGTH

    @property
    def nonce_length(self):
        """ Loosen limits. """
        return KEY_LENGTH

    @property
    def enforce_ssl(self):
        """ Allow unsafe access when using limited network. """
        return False

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce,
        request_token=None, access_token=None):
        """
        Should check if timestamp and nonce pair have been seen before.
        Here we trust the network and the client computer are completely secure.
        """
        return True

    def validate_client_key(self, client_key, request):
        return self.get_client_secret(client_key, request) is not None

    def get_client_secret(self, client_key, request):
        if client_key in self.__secrets:
            return self.__secrets[client_key]
        secret = LTIClient.objects.filter(key=client_key).first().secret
        self.__secrets[client_key] = secret
        return secret
