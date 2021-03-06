"""
Django settings for spring2020 project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import djcelery

djcelery.setup_loader()  ###
CELERY_TIMEZONE='Asia/Shanghai'  #并没有北京时区，与下面TIME_ZONE应该一致
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'django-cache'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l0@+7v14ago$4q-#&@wt9h7vwldddm9xg%d=@dhnzq)9uc@tfh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'report.apps.ReportConfig',
    'django_su',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'markdownify',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'django_tables2',
    'django_extensions',
    'rules.apps.AutodiscoverRulesConfig',
    'django_celery_results',
    'check'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'report.middleware.IPRecordMiddleware',
]

ROOT_URLCONF = 'spring2020.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_su.context_processors.is_su',
            ],
        },
    },
]

WSGI_APPLICATION = 'spring2020.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django_su.backends.SuBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MONTH_DAY_FORMAT = 'n月j日'
SHORT_DATETIME_FORMAT = 'n月j日 H:i'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploadfiles')


# Auth related settings

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

SU_LOGIN_REDIRECT_URL = '/admin/'
SU_LOGOUT_REDIRECT_URL = '/admin/'


# 3rd-party settings

BOOTSTRAP4 = {
    'css_url': '/static/css/bootstrap.min.css',
    'javascript_url': '/static/js/bootstrap.bundle.min.js',
    'theme_url': '/static/css/style.css',
    'jquery_url': '/static/js/jquery.min.js',
    'jquery_slim_url': '/static/js/jquery.slim.min.js',
    'popper_url': None,
}

PHONENUMBER_DEFAULT_REGION = 'CN'

MARKDOWNIFY_WHITELIST_TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre',
    'em', 'strong', 'code',
    'hr', 'br',
    'ul', 'ol', 'li',
    'a', 'img',
]
MARKDOWNIFY_WHITELIST_ATTRS = {
    'a': ['href', 'title'],
    'img': ['src', 'alt'],
}
MARKDOWNIFY_LINKIFY_PARSE_EMAIL = True


# Project settings

OAUTH_BASE_URL = 'https://stu.cs.tsinghua.edu.cn/api'
OAUTH_AUTHORIZE_URL = OAUTH_BASE_URL + '/v2/authorize'
OAUTH_ACCESS_TOKEN_URL = OAUTH_BASE_URL + '/v2/access_token'
OAUTH_REFRESH_TOKEN_URL = OAUTH_BASE_URL + '/v2/refresh_token'
OAUTH_USER_INFO_URL = OAUTH_BASE_URL + '/user/user_info'
OAUTH_PUSH_NOTIFICATION_URL = OAUTH_BASE_URL + '/notification/push'
OAUTH_CLIENT_ID = 'sU9TJl0IxmgMMa3q_YfP8T1HeuA'
OAUTH_CLIENT_SECRET = 'IHjFwjaPdn2iIqR5YHX6'

TSINGHUA_AUTH_LOGIN_URL = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/form/{appid_md5}/{seq}/?{callback_url}'
TSINGHUA_AUTH_AUTHORIZE_URL = 'https://id.tsinghua.edu.cn/thuser/authapi/checkticket/{appid}/{ticket}/{ipaddr}'

from datetime import timedelta
RECORD_OFFSET = timedelta(hours=-4)
ENTRY_OFFSET = timedelta(days=2)
