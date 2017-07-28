Example app using Django LTI Login
==================================

This is an example how to hook django-lti-login to a Django project.

Important parts are in `exampleapp/settings.py` and `exampleapp/urls.py`.
Those are required for django-lti-login to work.
Focus on lines that are marked with `XXX: for django-lti-login`.

In addition, you typically need receivers for signals.
See examples in `exampleapp/receivers.py` for how to do that.


Testing the example
-------------------

First, setup environment for you `virtualenv -p python3 venv`.
Second, install requirements `venv/bin/pip install -r ../requirements.txt`.
Last, create the sqlite database with `venv/bin/python manage.py migrate`.

Library exposes following management commands:

 * `./manage.py add_lti_key` for adding new keys
 * `./manage.py delete_lti_keys` for removing keys
 * `./manage.py list_lti_keys` and to list keys

Remember to create key with the first command.
You need the key and the secret for your learning management system.
In addition, you will need login url.
It's something like `http://localhost:8080/auth/lti_login`.

Ps. you can activate the virtualenv of course.
