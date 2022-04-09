"""Файл для создания админки."""
from django.contrib import admin

from .models import Langs, Video, AudioTrack, VideoTrack  # noqa: WPS300


@admin.register(Langs)
class LangsAdmin(admin.ModelAdmin):

    """
    Класс определяющий интерфейс редактирования языков.
    Присутствуют поля для отображения и поля для поиска.
    Модель Langs.
    """

    list_display = ('full_title', 'iso_639_1', 'created_at')
    search_fields = ('id', 'full_title', 'iso_639_1', 'iso_639_2')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):

    """
    Класс определяющий интерфейс редактирования видео.
    поля для отображения и поля для поиска.
    Модель Video.
    """

    list_display = ('title', 'updated_at')
    search_fields = ('title', 'id')


@admin.register(AudioTrack)
class AudioTrackAdmin(admin.ModelAdmin):

    """
    Класс определяющей интерфейс редактирования аудио трека.
    Поля для отображения и поля для поиска.
    Модель AudioTrackAdmin.
    """

    list_display = ('title', 'updated_at')
    search_fields = ('title', 'id')


@admin.register(VideoTrack)
class VideoTrackAdmin(admin.ModelAdmin):

    """
    Класс определяющей интерфейс редактирования видео трека.
    Поля для отображения и поля для поиска.
    Модель VideoTrackAdmin.
    """

    list_display = ('title', 'updated_at')
    search_fields = ('title', 'id')
