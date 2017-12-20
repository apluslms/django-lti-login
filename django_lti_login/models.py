from django.db import models
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from . import SAFE_CHARACTERS, KEY_LENGTH, SECRET_LENGTH
from .apps import app_settings


def word_validator(word, charset, length):
    if charset is not None and not frozenset(word).issubset(charset):
        raise ValidationError("Only following characters are allowed: '{}'".format("".join(charset)))
    minlen, maxlen = length
    if len(word) < minlen:
        raise ValidationError("Minimum length is {:d}.".format(minlen))
    if len(word) > maxlen:
        raise ValidationError("Maximum length is {:d}.".format(maxlen))

def create_new_key():
    return get_random_string(
        length=app_settings.KEY_LENGTH,
        allowed_chars=app_settings.KEY_CHARACTERS)

def create_new_secret():
    return get_random_string(
        length=app_settings.SECRET_LENGTH,
        allowed_chars=app_settings.SECRET_CHARACTERS)

def key_validator(key):
    return word_validator(key,
                          charset=SAFE_CHARACTERS,
                          length=KEY_LENGTH)

def secret_validator(secret):
    return word_validator(secret,
                          charset=None,
                          length=SECRET_LENGTH)


class LTIClient(models.Model):
    """
    A client service from which users can login to this service.
    """
    key = models.CharField(help_text='LTI client service key',
                           max_length=KEY_LENGTH[1],
                           default=create_new_key,
                           validators=[key_validator],
                           primary_key=True)
    secret = models.CharField(help_text='LTI client service secret',
                              max_length=SECRET_LENGTH[1],
                              default=create_new_secret,
                              validators=[secret_validator])
    description = models.TextField()

    class Meta:
        ordering = ['key']

    def __str__(self):
        desc = str(self.description)[:97]
        if len(desc) == 97:
            desc += '...'
        desc.replace('\n', ' ')
        return desc

    def __repr__(self):
        name = self.__class__.__name__
        return "<%s(key=%s): %s>" % (name, self.key, str(self))
