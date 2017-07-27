import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .apps import app_settings


logger = logging.getLogger('gjango_lti_login.backends')


class LTIAuthBackend(ModelBackend):
    """
    Authenticates the trusted user from the LTI request.
    """
    def authenticate(self, oauth_request=None):
        if not oauth_request:
            return None
        if not oauth_request.user_id:
            logger.warning('LTI login attempt without a user id.')
            return None

        UserModel = get_user_model()
        username_field = getattr(UserModel, 'USERNAME_FIELD', 'username')
        accepted_roles = app_settings.ACCEPTED_ROLES
        staff_roles = app_settings.STAFF_ROLES

        username_len = UserModel._meta.get_field(username_field).max_length
        email_len = UserModel._meta.get_field('email').max_length
        first_name_len = UserModel._meta.get_field('first_name').max_length
        last_name_len = UserModel._meta.get_field('last_name').max_length

        # get parameters and truncate to lengths that can be stored into database
        username = oauth_request.user_id[:username_len]
        email = oauth_request.lis_person_contact_email_primary[:email_len] or ''
        first_name = oauth_request.lis_person_name_given[:first_name_len] or ''
        last_name = oauth_request.lis_person_name_family[:last_name_len] or ''
        roles = frozenset(oauth_request.roles.split(',')) if oauth_request.roles else frozenset()

        if accepted_roles and roles.isdisjoint(accepted_roles):
            logger.warning('LTI login attempt without accepted user role: %s', roles)
            return None

        try:
            # get
            user = UserModel.objects.get(**{username_field: username})
            # update
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
        except UserModel.DoesNotExist:
            if not app_settings.CREATE_UNKNOWN_USER:
                return None

            # create new
            user = UserModel.objects.create_user(username, email, first_name=first_name, last_name=last_name)
            user.set_unusable_password()
            logger.info('Created a new LTI authenticated user: %s', user)

        user.is_staff = staff_roles and not roles.isdisjoint(staff_roles) or False
        user.save()

        logger.info('LTI authentication accepted for: %s', user)
        return user
