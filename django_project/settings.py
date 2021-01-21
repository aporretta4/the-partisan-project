"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import subprocess
from django_project.custom_aws.secrets import secrets_interactor
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

try:
    ENVORNMENT = os.getenv('PP_ENVIRONMENT')
    SECRET_KEY = secrets_interactor.getSecret(os.getenv('DJANGO_KEY_SECRET_NAME'))['secret_key']
    TW_BEARER_TOKEN = secrets_interactor.getSecret('pp_twitter_api')['bearer_token']
    REDDIT_APP_SECRET = secrets_interactor.getSecret('pp_reddit_api_secret')['secret_key']
    NYT_API_SECRET = secrets_interactor.getSecret('pp_nyt_news_api')['KEY']
    db_creds = secrets_interactor.getSecret(os.getenv('DB_PASS_SECRET_NAME'))
    DATABASES['default']['NAME'] = db_creds['dbname']
    DATABASES['default']['USER'] = db_creds['username']
    DATABASES['default']['PASSWORD'] = db_creds['password']
    DATABASES['default']['HOST'] = db_creds['host']
except:
    from django_project.local_settings import LOCAL_SECRET_KEY
    from django_project.local_settings import LOCAL_TW_BEARER_TOKEN
    from django_project.local_settings import LOCAL_ENVIRONMENT
    from django_project.local_settings import LOCAL_REDDIT_APP_SECRET
    from django_project.local_settings import LOCAL_NYT_API_KEY
    ENVORNMENT = LOCAL_ENVIRONMENT
    SECRET_KEY = LOCAL_SECRET_KEY
    TW_BEARER_TOKEN = LOCAL_TW_BEARER_TOKEN
    REDDIT_APP_SECRET = LOCAL_REDDIT_APP_SECRET
    NYT_API_SECRET = LOCAL_NYT_API_KEY
    from django_project.local_settings import LOCAL_DB_NAME
    from django_project.local_settings import LOCAL_DB_USER
    from django_project.local_settings import LOCAL_DB_PASS
    from django_project.local_settings import LOCAL_DB_HOST
    DATABASES['default']['NAME'] = LOCAL_DB_NAME
    DATABASES['default']['USER'] = LOCAL_DB_USER
    DATABASES['default']['PASSWORD'] = LOCAL_DB_PASS
    DATABASES['default']['HOST'] = LOCAL_DB_HOST

# SECURITY WARNING: don't run with debug turned on in production!
if ENVORNMENT != "Production":
    DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'partisan.apps.PartisanConfig'
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

ROOT_URLCONF = 'django_project.urls'

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

WSGI_APPLICATION = 'django_project.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True



# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "partisan/static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


ALLOWED_HOSTS = [
    '127.0.0.1',
    'ThePartisanProject-test2.us-west-2.elasticbeanstalk.com',
    '*'
]
