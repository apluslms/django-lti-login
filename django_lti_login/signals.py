from django.dispatch import Signal

lti_login_authenticated = Signal(providing_args=['request', 'user'])
