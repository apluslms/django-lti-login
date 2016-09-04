import logging
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from oauthlib.common import urlencode
from oauthlib.oauth1 import SignatureOnlyEndpoint

from . import LTIException
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

    endpoint = SignatureOnlyEndpoint(LTIRequestValidator())
    try:
        is_valid, oauth_request = endpoint.validate_request(uri, method, body, headers)

        if not is_valid:
            logger.warning('Invalid LTI login attempt.')
            raise LTIException('Not a valid LTI request')

        if oauth_request.lti_version != 'LTI-1p0' \
        or oauth_request.lti_message_type != 'basic-lti-launch-request':
            logger.warning('LTI login attempt without LTI 1.0 launch request.')
            raise LTIException('Not a valid LTI 1.0 launch request')

        user = authenticate(oauth_request=oauth_request)
        if not user:
            raise LTIException('No valid user found in the LTI request.')
        if not user.is_active:
            logger.warning('LTI login attempt for inactive user: %s', user.username)
            raise LTIException('The user is not active.')

        request.oauth = oauth_request
        login(request, user)
        logger.debug('LTI authenticated user logged in: %s', user.username)

        return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))

    except LTIException as e:
        return HttpResponse(e.message, content_type='text/plain', status=403)
