from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import check_for_language
from .apps import app_settings


LANGUAGE_COOKIE_NAME = settings.LANGUAGE_COOKIE_NAME
LANGUAGE_COOKIE_ARGS = dict(
    max_age=settings.LANGUAGE_COOKIE_AGE,
    path=settings.LANGUAGE_COOKIE_PATH,
    domain=settings.LANGUAGE_COOKIE_DOMAIN,
)


def set_user_language_from_lti(sender, **kwargs):
    try:
        request = kwargs['request']
        user = kwargs['user']
        oauth = request.oauth
        language = oauth.launch_presentation_locale
    except (KeyError, AttributeError):
        return None

    if not language or not check_for_language(language):
        return None

    if LANGUAGE_COOKIE_NAME not in request.COOKIES:
        oauth.set_cookies.append((
            (LANGUAGE_COOKIE_NAME, language),
            LANGUAGE_COOKIE_ARGS,
        ))

if app_settings.SET_LANGUAGE:
    user_logged_in.connect(set_user_language_from_lti)
