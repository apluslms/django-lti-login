Django LTI login
================

A simple, yet powerful, LTI login application for Django.
This app makes it easy to use learning management system (LMS) with LTI 1.0 interface to authenticate users to external services.

Installation
------------

Run :code:`pip install git+https://github.com/Aalto-LeTech/django-lti-login.git@master#egg=django-lti-login`.

Add :code:`django_lti_login` to :code:`settings.INSTALLED_APPS`.

Add :code:`django_lti_login.backends.LTIAuthBackend` to :code:`settings.AUTHENTICATION_BACKENDS`.

Examinate project in :code:`example` directory for more detailed example.
Most relevant parts are marked with :code:`XXX: for django-lti-login`.

Usage
-----

After you have configured your project with settings and lti tokens,
then you can point your LMS to the :code:`lti_login` url (see example app).
Remember those lti tokens (a key and a secret).
App provides django management commands to handle those tokens.
