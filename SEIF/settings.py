"""
Django settings base for SEIF project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from shutil import which
import dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from . import ckeditor_config, logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SEIF_ENV_OPTIONS = {"development": ".env.dev", "production": ".env.prod"}

# Configuring environment variables
dotenv.load_dotenv(".env")
SEIF_ENV = os.getenv("SEIF_ENV", "default")
ENV_VARS_FILE = SEIF_ENV_OPTIONS.get(SEIF_ENV, ".env")

env_path = dotenv.find_dotenv(ENV_VARS_FILE)
if env_path is None:
    raise FileNotFoundError(
        f"Could not find {ENV_VARS_FILE} file. Please make sure you have a \
        {ENV_VARS_FILE} file in your project root."
    )

dotenv.load_dotenv(env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

NPM_BIN_PATH = which("npm")

# Set the Logging configuration
LOGGING = logging.LOGGING

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-q203iv@f+*r=hd-^s4m5g1$2i%o+jr8r0_s3!o5@68j$8%-*7^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "tailwind",
    "theme",
    "django_browser_reload",
    "dj_svg",
    "django_ckeditor_5",
    # local apps
    "core",
    "accounts",
    "management",
    "utils",
]

TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = ["127.0.0.1"]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "SEIF.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "SEIF.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "USER": os.getenv("DB_USER"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "core/static"),
    os.path.join(BASE_DIR, "management/static"),
]

CKEDITOR_5_CONFIGS = ckeditor_config.CKEDITOR_5_CONFIGS
CKEDITOR_5_FILE_UPLOAD_PERMISSION = ckeditor_config.CKEDITOR_5_FILE_UPLOAD_PERMISSION
CKEDITOR_5_CUSTOM_CSS = ckeditor_config.CKEDITOR_5_CUSTOM_CSS

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom admin user
AUTH_USER_MODEL = "accounts.Participant"


sentry_sdk.init(
    dsn="https://2d35e61739e25ec7bdf5d035f80f0d32@o4504842400628736.ingest.us.sentry.io/\
    4508807608205312",
    integrations=[DjangoIntegration()],
    send_default_pii=True,  # This enables sending personally identifiable information if needed
    traces_sample_rate=1.0,  # This captures all transactions for tracing
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)
