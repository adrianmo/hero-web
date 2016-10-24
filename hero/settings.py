"""
Django settings for hero project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from configurations import Configuration, values


class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '7cws4r3wk#fzry)(s1#_@^%l5o-lbqft8=@uq-y=-$m$87crlp'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'bootstrap_themes',
        'bootstrap3',
        'django_countries',
        'formtools',
        'anymail',
        'app',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'hero.urls'

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

    WSGI_APPLICATION = 'hero.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.10/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 9,
            },
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.10/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Hero Game

    HERO_API = os.getenv('HERO_API', '')
    HERO_ADMIN_TOKEN = os.getenv('HERO_ADMIN_TOKEN', '')
    NEUTRINO_URL = os.getenv('NEUTRINO_URL', '')
    HORIZON_URL = os.getenv('HORIZON_URL', '')


class Dev(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True


class Prod(Common):
    """
    The in-production settings.
    """
    ALLOWED_HOSTS = ["*"]

    # Check needed env vars
    if not Common.DEBUG:
        env_vars = ['HERO_API', 'HERO_ADMIN_TOKEN', 'NEUTRINO_URL', 'MAILGUN_API_KEY',
                    'MAILGUN_SENDER_DOMAIN', 'DEFAULT_FROM_EMAIL', 'DATABASE_URL']
        for env_var in env_vars:
            assert env_var in os.environ, "{} environment variable is not set".format(env_var)

    # Mailgun

    ANYMAIL = {
        "MAILGUN_API_KEY": os.getenv('MAILGUN_API_KEY', ''),
        "MAILGUN_SENDER_DOMAIN": os.getenv('MAILGUN_SENDER_DOMAIN', ''),
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', '')

    # Update database configuration with $DATABASE_URL.

    import dj_database_url
    db_from_env = dj_database_url.config()
    db_from_env['OPTIONS'] = {}
    Common.DATABASES['default'].update(db_from_env)

    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    # STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
