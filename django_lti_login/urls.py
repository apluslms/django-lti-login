"""
Url definitions for django-lti-login

Should add something like following to project urls.py:

    url(r'^auth/', include('django_lti_login.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')), # for reference

"""
from django.urls import re_path

from .views import lti_login

urlpatterns = [
    re_path(r'^lti_login/?$', lti_login, name='lti_login'),
]
