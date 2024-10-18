"""
A configuration for the django-cors-headers module. CORS is necessary for being able to
work with a separate front end (e.g. React, Vue, whatever). It basically allows a front
end to make requests to your back end.

Read more here: https://github.com/adamchainz/django-cors-headers/

=========================
=== ADDITIONAL CONFIG ===
=========================

The `corsheaders` app has been registered in config.django.base.
The `corsheaders.middleware.CorsMiddleware` middleware has been registered as well.

The position of the middleware is important. It has to be near the top, currently
positioned after `django.middleware.security.SecurityMiddleware`.

Some of the settings below are overridden in config.django.production.
"""

from config.env import env

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

BASE_BACKEND_URL = env.str("DJANGO_BASE_BACKEND_URL", default="http://localhost:8000")
BASE_FRONTEND_URL = env.str("DJANGO_BASE_FRONTEND_URL", default="http://localhost:3000")
CORS_ORIGIN_WHITELIST = env.list(
    "DJANGO_CORS_ORIGIN_WHITELIST", default=[BASE_FRONTEND_URL]
)
