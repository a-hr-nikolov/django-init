from config.env import BASE_DIR, env

# Build paths inside the project like this: BASE_DIR / 'subdir'.

env.read_env(BASE_DIR / ".env")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
DEBUG = env.bool("DJANGO_DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY")


########################################################################################
#
# APPLICATION DEFINITION & DJANGO-RELATED CONFIG
#
########################################################################################

LOCAL_APP_DIR_PREFIX = "apps."

LOCAL_APPS = [
    # ================================ IMPORTANT !!!! ==================================
    # List only the app names, not their dotted path.
    # For example, don't do "my_apps_directory.my_app", instead simply list "my_app".
    # ==================================================================================
    "api",
    "common",
    "users",
]

LOCAL_APPS = [LOCAL_APP_DIR_PREFIX + app for app in LOCAL_APPS]


THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "django_filters",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    # "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


########################################################################################
#
# DATABASE
#
########################################################################################
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
########################################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     "default": env.db("DATABASE_URL", default="postgres:///example"),
# }

# if os.environ.get("GITHUB_WORKFLOW"):
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": "github_actions",
#             "USER": "postgres",
#             "PASSWORD": "postgres",
#             "HOST": "127.0.0.1",
#             "PORT": "5432",
#         }
#     }
# DATABASES["default"]["ATOMIC_REQUESTS"] = True


########################################################################################
#
# AUTH & PASSWORD VALIDATION
#
########################################################################################
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
########################################################################################

AUTH_USER_MODEL = "users.BaseUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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


########################################################################################
#
# INTERNATIONALIZATION
#
########################################################################################
# https://docs.djangoproject.com/en/stable/topics/i18n/
########################################################################################

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


########################################################################################
#
# STATIC FILES (CSS, JavaScript, Images)
#
########################################################################################
# https://docs.djangoproject.com/en/stable/howto/static-files/
########################################################################################

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


########################################################################################
#
# CACHE
#
########################################################################################
# https://docs.djangoproject.com/en/stable/topics/cache/
########################################################################################
# OPTIONS: https://docs.djangoproject.com/en/stable/topics/cache/#cache-arguments
# Per-site vs Per-view: https://docs.djangoproject.com/en/stable/topics/cache/#the-per-site-cache
#
#
# In-Memory:
#   Memcached: https://docs.djangoproject.com/en/stable/topics/cache/#memcached
#   Redis: https://docs.djangoproject.com/en/stable/topics/cache/#redis
#
# Dev:
#   LocMem: https://docs.djangoproject.com/en/stable/topics/cache/#local-memory-caching
#   Dummy: https://docs.djangoproject.com/en/stable/topics/cache/#dummy-caching-for-development
#
# Disk:
#   Database: https://docs.djangoproject.com/en/stable/topics/cache/#database-caching
#   Filesystem: https://docs.djangoproject.com/en/stable/topics/cache/#filesystem-caching
#
# Custom:
# https://docs.djangoproject.com/en/stable/topics/cache/#using-a-custom-cache-backend
########################################################################################

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        # "LOCATION": "unique-snowflake",
    }
}

# ==================================== MEMCACHED =======================================
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
#         # "BACKEND": django.core.cache.backends.memcached.PyLibMCCache,
#         "LOCATION": "127.0.0.1:11211",
#     }
# }

# ====================================== REDIS =========================================
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://username:password@127.0.0.1:6379",
#     }
# }

# CACHE_MIDDLEWARE_ALIAS = "default"
# CACHE_MIDDLEWARE_SECONDS = 600
# CACHE_MIDDLEWARE_KEY_PREFIX = "my_website"


########################################################################################
#
# LOGGING
#
########################################################################################
# https://docs.djangoproject.com/en/stable/topics/logging/
########################################################################################
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "root": {"handlers": ["console", "mail_admins"]},
    },
}


########################################################################################
#
# REST FRAMEWORK
#
########################################################################################
# https://www.django-rest-framework.org/api-guide/settings/
########################################################################################

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "apps.api.exception_handlers.improved_exception_handler",
    # "EXCEPTION_HANDLER": "apps.api.exception_handlers.simple_mapping_exception_handler",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    # "DEFAULT_AUTHENTICATION_CLASSES": [],
}


########################################################################################
#
# THIRD PARTY CONFIG
#
########################################################################################

# from config.settings.celery import *  # noqa
from config.settings.cors import *  # noqa
# from config.settings.email_sending import *  # noqa
# from config.settings.files_and_storages import *  # noqa
# from config.settings.google_oauth2 import *  # noqa
# from config.settings.jwt import *  # noqa
# from config.settings.sentry import *  # noqa
# from config.settings.sessions import *  # noqa

# from config.settings.debug_toolbar.settings import *  # noqa
# from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa

# INSTALLED_APPS, MIDDLEWARE = DebugToolbarSetup.do_settings(INSTALLED_APPS, MIDDLEWARE)
