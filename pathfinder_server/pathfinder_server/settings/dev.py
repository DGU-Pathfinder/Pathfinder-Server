from .common import *

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]

CORS_ORIGIN_WHITE_LIST = ["http://localhost:3000"]

CELERY_BROKER_URL = get_env_variable("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = get_env_variable("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESYULT_SERIALIZER = "json"