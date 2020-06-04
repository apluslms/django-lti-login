import sys
from os.path import dirname, abspath, join

BASE_DIR = dirname(dirname(abspath(__file__)))
# Following is here so we can access the django_lti_login from current clone of the repo
ROOT_DIR = dirname(BASE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(1, ROOT_DIR)

# Basic stuff
SECRET_KEY = 'not so secret key'
DEBUG = True
ALLOWED_HOSTS = []
ROOT_URLCONF = 'exampleapp.urls'
STATIC_URL = '/static/'
WSGI_APPLICATION = 'wsgi.application'
LOGIN_REDIRECT_URL = 'frontpage'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_lti_login', # XXX: for django-lti-login
    'exampleapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'example.db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = [
    'django_lti_login.backends.LTIAuthBackend', # XXX: for django-lti-login
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

# XXX: for django-lti-login
AUTH_LTI_LOGIN = {
    # e.g. roles: Instructor, TeachingAssistant, Student
    'ACCEPTED_ROLES': None, # Allow with any role
    'STAFF_ROLES': ['Instructor'], # set is_staff=True for teachers.
    # read more from django_lti_login.apps.app_settings
}
