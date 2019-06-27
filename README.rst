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


A LTI key management API
------------------------

You can enable a simple LTI key management API, by configuring JWT authentication secrets.

For ``RS256`` and related algorithms you need to provide a public key in PEM format.
For example:

.. code-block:: python

    LTI_JWT_PUBKEY = """
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw4GPplGOEcfw/Hg9rBU3
    OFR/ykB68Z5AF0nRMgUYEu9gHcfSePF+ut/PwXiwvCEugVHsTUZb4t1JgdYOZHx/
    bODxyIWco7t8UsgokpOVetDqnv1quW6UN2bsQRdzmOhTjdvZJUWF6JJq7RLnry0U
    O/kCCD1EsWOkFPia47tbcSVKmF+FTZiWI26Wv34LymDjFz3APsH6p1zMEM1CRWZ6
    XMZofGdxcIjSCrU5zel/SE24lTr0IPLbEFlrzIT1EkvEMap42vLvix8z0E1VB/Ro
    LgcE1AOYq/Cwv+YKBxciDgMmct1E98f48e/P2yA0tf8nAKCKrN8qqn1Tv/KQ1u7L
    0wIDAQAB
    -----END PUBLIC KEY-----
    """

Public key algorithms require the ``cryptography`` library, which can be installed using extra requirements.
For example: ``pip3 install git+https://github.com/Aalto-LeTech/django-lti-login.git@master#egg=django-lti-login[crypto]``.

For ``HS256`` and related algorithms you need just the shared secret key.
The secret key must be base64 encoded binary and at least 256 bits / 32 bytes long when decoded.
For example:

.. code-block:: python

    LTI_JWT_SECRET = "SFA9apySMOTIi+g0Skj/cgq/5ELN7pyze7T+JuSMM5Q="

In addition, you can restrict the issuer and the audience fields:

.. code-block:: python

    LTI_JWT_ISSUER = "my.domain.com"
    LTI_JWT_AUDIENCE = "administrator"


**NOTE**: Only one of ``LTI_JWT_PUBKEY`` or ``LTI_JWT_SECRET`` can be used at a time.

The api supports following actions:

* ``GET /lti_api/`` - list all keys and their data
* ``GET /lti_api/{key}`` - return the secret and the description of a key ``{key}``
* ``PUT /lti_api/{key}`` - create or update a key and it's data
* ``DELETE /lti_api/{key}`` - delete an existing key from the database

For development, you can create keys on `JWT.io <https://jwt.io/>`_.

.. code-block:: sh

    token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9Cg.eyJzdWIiOiJ1c2VyIiwiaXNzIjoibXkuZG9tYWluLmNvbSIsImp3aSI6ImFiNDRkNjlmLWU4OGYtNDE1ZC04ODE0LTNmMmEwOTM1Y2FiNCIsImlhdCI6MTU2MTY3ODU3MSwiZXhwIjoxNTY0MjcwNTcxfQo.lEi2LX0f_7fL_coGn2kElQsXPVcKSGuiLq1afDNY8Ck"

    # list all keys
    $ curl -H "Authorization: bearer $token" http://localhost/lti_api | jq
    {
      "count": 0,
      "results": []
    }

    # add a new key
    $ curl -H "Authorization: bearer $token" -X PUT http://localhost/lti_api/new_key | jq
    {
      "key": "new_key",
      "desc": "key added by user@my.domain.com",
      "secret": "rLxM7ZE4yESz1vdrywXmuTxZf2b4K2SCDkSTZn0ptMXgpKg37mrbKH9pZxO7prj7"
    }

    # add a new key with secret
    $ curl -H "Authorization: bearer $token" -X PUT -d secret=top_secret http://localhost/lti_api/second_key | jq
    {
      "key": "second_key",
      "desc": "key added by user@my.domain.com",
      "secret": "top_secret"
    }

    # delete a key
    $ curl -H "Authorization: bearer $token" -X DELETE http://localhost/lti_api/second_key | jq
    {
      "key": "second_key",
      "desc": "key added by user@my.domain.com",
      "secret": "top_secret"
    }
