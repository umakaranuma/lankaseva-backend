"""
Django settings for the LankaSeva backend.

All Django default contrib apps (admin, auth, sessions, contenttypes, messages)
are intentionally NOT installed so that the database contains only the
project's own tables (users, auth_tokens, otp_codes, services, service_phones,
opening_hours, reviews, review_tags).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')

DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '*').split(',') if h.strip()]

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'accounts',
    'services',
    'reviews',
    'emergency',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = []

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + os.getenv('DB_CONNECTION', 'mysql'),
        'NAME': os.getenv('DB_DATABASE', 'lankaseva'),
        'USER': os.getenv('DB_USERNAME', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Our own user table (accounts_users) — Django's auth_user is never created.
AUTH_USER_MODEL = 'accounts.AppUser'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'accounts.authentication.AppTokenAuthentication',
    ],
    # The default (django.contrib.auth.models.AnonymousUser) needs the
    # contenttypes app, which is intentionally not installed.
    'UNAUTHENTICATED_USER': 'accounts.authentication.AnonymousUser',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'config.pagination.DefaultPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '120/min',
        'otp': '5/min',
    },
}

OTP_EXPIRY_MINUTES = int(os.getenv('OTP_EXPIRY_MINUTES', '5'))

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Colombo'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
