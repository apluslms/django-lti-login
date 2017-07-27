import logging
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from oauthlib.common import urlencode
from oauthlib.oauth1 import SignatureOnlyEndpoint

from .signals import lti_login_authenticated
from .validators import LTIRequestValidator



logger = logging.getLogger('django_lti_login.views')


@csrf_exempt
@require_http_methods(["POST"])
def lti_login(request):
    """
    Accepts LTI launch requests and logs in matching local users.
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
        logger.warning('Invalid LTI login attempt.')
        raise PermissionDenied('Not a valid LTI request')

    if oauth_request.lti_version != 'LTI-1p0' \
    or oauth_request.lti_message_type != 'basic-lti-launch-request':
        logger.warning('LTI login attempt without LTI 1.0 launch request.')
        raise PermissionDenied('Not a valid LTI 1.0 launch request')

    # authenticate user
    user = authenticate(oauth_request=oauth_request)
    if not user:
        raise PermissionDenied('No valid user found in the LTI request.')
    if not user.is_active:
        logger.warning('LTI login attempt for inactive user: %s', user)
        raise PermissionDenied('The user is not active.')

    # Set vars for listenters
    request.oauth = oauth_request
    oauth_request.redirect_url = settings.LOGIN_REDIRECT_URL
    oauth_request.set_cookies = []

    # signal that authentication step has been done
    lti_login_authenticated.send(sender=user.__class__, request=request, user=user)

    # login the user (sends signal user_logged_in)
    login(request, user)

    # Create redirect response
    response = redirect(oauth_request.redirect_url)

    # set possible cookies
    for args, kwargs in oauth_request.set_cookies:
        response.set_cookie(*args, **kwargs)

    logger.debug('Logged in a LTI authenticated user: %s', user)
    return response
