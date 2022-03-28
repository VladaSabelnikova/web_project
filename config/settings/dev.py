"""Файл настройки админки в формате разработки."""

from .base import *  # noqa: F401,F403,WPS347,WPS300

DEBUG = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
