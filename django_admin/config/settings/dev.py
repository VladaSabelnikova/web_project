"""Файл настройки админки в формате разработки."""

from .base import *  # noqa: F401,F403,WPS347,WPS300

DEBUG = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # noqa: F405
# ALLOWED_HOSTS = [os.getenv('DB_HOST', '127.0.0.1')]