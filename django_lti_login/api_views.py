import binascii
import logging
from base64 import b64decode
from collections.abc import Mapping
from functools import partial
from json import loads

import jwt
from django.conf import settings
from django.core.exceptions import (
    ImproperlyConfigured,
    PermissionDenied,
    ValidationError,
)
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse,
)
from django.http.multipartparser import MultiPartParser
from django.http.request import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import (
    LTIClient,
    create_new_secret,
    key_validator,
)


logger = logging.getLogger(__name__)


def setting_in_bytes(name):
    value = getattr(settings, name)
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode('utf-8')
    raise ImproperlyConfigured(
        "Value for settings.%s is not bytes or str."
        % (name,))


def prepare_decoder():
    options = {'verify_'+k: True for k in ('iat', 'nbf', 'exp', 'iss', 'aud')}
    options.update({'require_'+k: True for k in ('iat',)})
    if hasattr(settings, 'LTI_JWT_ISSUER'):
        options['issuer'] = settings.LTI_JWT_ISSUER
    if hasattr(settings, 'LTI_JWT_AUDIENCE'):
        options['audience'] = settings.LTI_JWT_AUDIENCE
    if hasattr(settings, 'LTI_JWT_PUBKEY') and hasattr(settings, 'LTI_JWT_SECRET'):
        raise ImproperlyConfigured(
            "Only one of LTI_JWT_PUBKEY or LTI_JWT_SECRET can be defined at "
            "a time.")
    if hasattr(settings, 'LTI_JWT_PUBKEY'):
        try:
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives.serialization import load_pem_public_key
        except ImportError as error:
            raise ImproperlyConfigured(
                "`django_lti_login` requires `cryptography` when using settings.LTI_JWT_PUBKEY: %s"
                % (error,))
        pem = setting_in_bytes('LTI_JWT_PUBKEY')
        try:
            key = load_pem_public_key(pem, backend=default_backend())
        except ValueError as error:
            raise ImproperlyConfigured(
                "Invalid public key in LTI_JWT_PUBKEY: %s"
                % (error,))
        return partial(jwt.decode,
            key=key,
            algorithms=['RS256', 'RS384', 'RS512'],
            **options)
    elif hasattr(settings, 'LTI_JWT_SECRET'):
        try:
            key = b64decode(setting_in_bytes('LTI_JWT_SECRET'), validate=True)
        except binascii.Error as error:
            raise ImproperlyConfigured(
                "Invalid secret key in LTI_JWT_SECRET: %s"
                % (error,))
        if len(key) < 32:
            if not settings.DEBUG:
                raise ImproperlyConfigured(
                    "The secret key in LTI_JWT_SECRET is less than 32 bytes")
            logger.warning("The secret key in LTI_JWT_SECRET is less than "
                           "32 bytes. This raises error in production, but "
                           "it is allowed in DEBUG mode.")
        return partial(jwt.decode,
            key=key,
            algorithms=['HS256', 'HS384', 'HS512'],
            **options)
    return None

jwt_decode = prepare_decoder()


def jwt_auth(request):
    if prepare_decoder is None:
        raise ImproperlyConfigured(
            "Received request to %s.lti_api without LTI_JWT_PUBKEY or "
            "LTI_JWT_SECRET in django settings."
            % (__name__,))

    # require authentication header
    if 'HTTP_AUTHORIZATION' not in request.META:
        logger.debug("JWT auth failed: No authorization header")
        raise PermissionDenied("No authorization header")
    try:
        scheme, token = request.META['HTTP_AUTHORIZATION'].strip().split(' ', 1)
        if scheme.lower() != 'bearer': raise ValueError()
    except ValueError:
        logger.debug("JWT auth failed: Invalid authorization header: %r",
            request.META.get('HTTP_AUTHORIZATION', ''))
        raise PermissionDenied("Invalid authorization header")

    # decode jwt token
    try:
        return jwt_decode(token)
    except jwt.InvalidTokenError as exc:
        logger.debug("JWT auth failed: %s", exc)
        raise PermissionDenied(str(exc))


@require_http_methods(['GET'])
def lti_api_list(request, key=None):
    auth = jwt_auth(request)

    records = [
        {'key': record.key,
         'secret': record.secret,
         'desc': record.description}
        for record in LTIClient.objects.all()
    ]
    return JsonResponse({
        'count': len(records),
        'results': records,
    })


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def lti_api_record(request, key):
    auth = jwt_auth(request)

    # get previous record
    try:
        key_validator(key)
    except ValidationError as exc:
        logger.debug("Invalid key: %s", exc)
        return HttpResponseNotFound()
    try:
        record = LTIClient.objects.get(key=key)
    except LTIClient.DoesNotExist:
        record = None

    # get
    if request.method == 'GET':
        if record is None:
            return HttpResponseNotFound()

    # create / update
    elif request.method == 'PUT':
        # parse data (not done by Django for PUT)
        content_type = request.META['CONTENT_TYPE']
        if content_type == 'application/x-www-form-urlencoded':
            data = QueryDict(request.body, encoding=request.encoding)
        elif content_type.startswith('multipart/form-data'):
            parser = MultiPartParser(request.META, request, request.upload_handlers, request.encoding)
            data, _files = parser.parse()
        elif content_type == 'application/json' or \
                (content_type.startswith('application/') and content_type.endswith('+json')):
            try:
                data = loads(request.body.decode(request.encoding or 'utf-8'))
            except ValueError:
                return HttpResponseBadRequest("Malformed json data")
            if not isinstance(data, Mapping):
                return HttpResponseBadRequest("Invalid json data type")
        elif content_type == 'text/plain':
            data = {}
            if request.body:
                data['secret'] = request.body
        else:
            logger.warning(content_type)
            return HttpResponseBadRequest("Unsupported content-type")

        if not record:
            record = LTIClient(key=key)

        if 'secret' in data:
            record.secret = data['secret']
        elif not record.secret:
            record.secret = create_new_secret()
        if 'desc' in data:
            record.description = data['desc']
        elif not record.description:
            record.description = "key added by %s@%s" % (
                auth.get('sub', ''), auth.get('iss', ''))

        try:
            record.full_clean()
        except ValidationError as error:
            return HttpResponseBadRequest("Data is not valid: %s" % (error,))

        record.save()

    # delete
    if request.method == 'DELETE':
        if record is None:
            return HttpResponseNotFound()
        record.delete()

    return JsonResponse({
        'key': key,
        'secret': record.secret,
        'desc': record.description,
    })
