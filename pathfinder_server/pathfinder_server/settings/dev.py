from .common import *
from corsheaders.defaults import default_headers

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]

# CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # "127.0.0.1:3000"
]

CORS_ALLOW_HEADERS = [
    *default_headers,
    'Access-Control-Allow-Origin',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Methods',
    'withCredentials',
]

# CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
# CORS_ALLOW_ALL_ORIGINS = True

CELERY_BROKER_URL = get_env_variable("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = get_env_variable("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESYULT_SERIALIZER = "json"