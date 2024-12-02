"""
Django settings for quiz_backend project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-11d2@t0hg3a1ief_%115^76i^8+ree(hv7157u)dbyf!4c%rix'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'room',
    'quiz',
    'invitation',
    'rest_framework',
    'rest_api',
    # 'rest_framework_swagger',
    'drf_spectacular',
    'drf_yasg',
    'corsheaders',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.TokenAuthentication',
    # ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ),

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# REST_FRAMEWORK = {

#     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
#     'DEFAULT_PAGINATION_CLASS': 'belgorodshop.share.paginations.TotalPageNumberPagination',
#     'PAGE_SIZE': 30,
# }

SPECTACULAR_SETTINGS = {
    'TITLE': 'Quiz Project API',
    'DESCRIPTION': 'Отсюда тырить api',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # 'SWAGGER_UI_SETTINGS': {
    #     'persistAuthorization': True,
    # },
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
    # 'AUTHENTICATION_WHITELIST': ["rest_framework.authentication.TokenAuthentication"],
    # 'SECURITY': [
    #     {'TokenAuth': []},
    # ],
    # 'COMPONENTS': {
    #     'securitySchemes': {
    #         'TokenAuth': {
    #             'type': 'apiKey',
    #             'in': 'header',
    #             'name': 'Authorization',
    #             'description': 'вводится в такой форме "Token <your_token>".',
    #         }
    #     },
    # },
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'quiz_backend.urls'

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

WSGI_APPLICATION = 'quiz_backend.wsgi.application'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(weeks=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(weeks=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LAZY': timedelta(weeks=1),
    'SLIDING_TOKEN_LIFETIME_LAZY': timedelta(weeks=1),
    'ROTATE_REFRESH_TOKENS': True,
}
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz',
        'USER': 'developer',
        'PASSWORD': 'gIErkL',
        'HOST': '185.128.105.41',
        'PORT': '5433',
        'TEST': {
            'NAME': 'test_quiz',
            # 'CHARSET': 'UTF8',
        },
    }
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',
    #     }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

# CORS_ALLOWED_ORIGIN = ["*"]

CORS_ALLOW_ALL_ORIGIN = True

CORS_ALLOW_CREDENTIALS = True
