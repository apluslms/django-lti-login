from django.dispatch import Signal

""" Sender should provide 'request' and 'user' arguments."""
lti_login_authenticated = Signal()
