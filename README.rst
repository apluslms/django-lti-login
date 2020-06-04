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

Example and test application
----------------------------

An example application is provided in the `example <example/>`_ directory.
In addition, the example is packaged as a Docker image in `docker hub / apluslms / run-lti-example <docker run-lti-example_>`_.
To use the image with `A+ <aplus_>`_, you need to add the following snipped to the course docker-compose.yml_.

.. _aplus: https://apluslms.github.io
.. _docker run-lti-example: https://hub.docker.com/r/apluslms/run-lti-example/
.. _docker-compose.yml: https://github.com/apluslms/course-templates/blob/master/docker-compose.yml

.. code-block:: yaml

  # add to 'services'
  lti:
    image: apluslms/run-lti-example
    volumes:
      - data:/data
    depends_on:
      - grader
      - plus
