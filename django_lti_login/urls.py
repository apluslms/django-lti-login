"""
Url definitions for django-lti-login

Should add something like following to project urls.py:

    url(r'^auth/', include('django_lti_login.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')), # for reference

"""
from django.conf.urls import url

from . import api_views
from .views import lti_login

urlpatterns = (
    url(r'^lti_login/?$', lti_login, name='lti_login'),
    )

if api_views.jwt_decode is not None:
    urlpatterns += (
        url(r'^lti_api/?$', api_views.lti_api_list, name='lti_api_list'),
        url(r'^lti_api/(?P<key>[^/]+)/?$', api_views.lti_api_record, name='lti_api_record'),
    )
