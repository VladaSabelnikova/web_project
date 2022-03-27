"""Файл для создания приложений."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VideosConfig(AppConfig):

    """
    Класс для создания приложений.
    В данном случае приложение у нас одно (videos).
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos'
    verbose_name = _('videos')
