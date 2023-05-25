import logging
from urllib.parse import urlsplit

from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from oauthlib.common import urlencode
from oauthlib.oauth1 import SignatureOnlyEndpoint

from .signals import lti_login_authenticated
from .validators import LTIRequestValidator


logger = logging.getLogger('django_lti_login.views')


@csrf_exempt
@require_http_methods(["POST"])
def lti_login(request):
    """
    Accepts LTI launch requests
    """
    # Extract request data for oauthlib.
    uri = request.build_absolute_uri()
    method = request.method
    body = urlencode(request.POST.items())
    headers = {k: v for k, v in request.META.items() if not k.startswith('wsgi.')}
    if 'HTTP_AUTHORIZATION' in headers:
        headers['Authorization'] = headers['HTTP_AUTHORIZATION']
    if 'CONTENT_TYPE' in headers:
        headers['Content-Type'] = headers['CONTENT_TYPE']

    # create oauth endpoint and validate request
    endpoint = SignatureOnlyEndpoint(LTIRequestValidator())
    is_valid, oauth_request = endpoint.validate_request(uri, method, body, headers)

    if not is_valid:
        logger.warning('An invalid LTI login request. Are the tokens configured correctly?')
        raise PermissionDenied('An invalid LTI login request. Are the tokens configured correctly?')

    if (oauth_request.lti_version != 'LTI-1p0' or
        oauth_request.lti_message_type != 'basic-lti-launch-request'):
        logger.warning('A LTI login request is not LTI-1p0 or basic-lti-launch-request.')
        raise PermissionDenied('Version is not LTI-1p0 or type is not basic-lti-launch-request for a LTI login request.')

    # authenticate user
    user = authenticate(request, oauth_request=oauth_request)
    if not user:
        raise PermissionDenied('Authentication of a LTI request did not yield an user')
    if not user.is_active:
        logger.warning('A LTI login attempt by inactive user: %s', user)
        raise PermissionDenied('An authenticated user is not active')

    # Set vars for listenters
    request.oauth = oauth_request
    oauth_request.redirect_url = None
    oauth_request.set_cookies = []

    # signal that authentication step has been done
    lti_login_authenticated.send(sender=user.__class__, request=request, user=user)

    # login the user (sends signal user_logged_in)
    login(request, user)

    # Create redirect response
    redirect_to = oauth_request.redirect_url
    if redirect_to and not url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
            ):
        redirect_to = None
    if redirect_to is None:
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
    response = HttpResponseRedirect(redirect_to)

    # set possible cookies
    for args, kwargs in oauth_request.set_cookies:
        response.set_cookie(*args, **kwargs)

    logger.debug('Login completed for a LTI authenticated user: %s', user)
    return response
