import string


GOOD_CHARACTERS = string.ascii_letters + string.digits
SAFE_CHARACTERS = GOOD_CHARACTERS + '-'
SAFE_CHARACTERS_SET = frozenset(SAFE_CHARACTERS)
KEY_LENGTH = 6, 128


def accept_course(oauth_request, user):
    import logging
    logger = logging.getLogger('gjango_lti_login')
    from data.models import Course, URLKeyField
    """
    Creates or gets the course instance and adds user to it.
    """

    course_key = URLKeyField.safe_version(oauth_request.context_id) \
        if oauth_request.context_id else None
    course_name = oauth_request.context_title \
        if oauth_request.context_title else ''

    if course_key:
        course, created = Course.objects.get_or_create(key=course_key,
            defaults={'name': course_name, 'provider': 'a+', 'tokenizer': 'scala' })
        if created:
            logger.info('Creating a new LTI authenticated course: %s', course_name)
        course.reviewers.add(user)


