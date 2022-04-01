"""Файл для создания админки."""

from django.contrib import admin

from .models import Langs, Video, AudioAndText  # noqa: WPS300


class AudioAndTextInline(admin.TabularInline):
    """
    Класс для вставки аудио и текста со страницы редактирования видео.
    Модель AudioAndText.
    """

    model = AudioAndText


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
    Присутствуют интерфейс для редактирования аудио и теста,
    поля для отображения и поля для поиска.
    Модель Video.
    """

    inlines = (AudioAndTextInline,)
    list_display = ('video_file', 'updated_at')
    search_fields = ('id',)


@admin.register(AudioAndText)
class AudioAndTextAdmin(admin.ModelAdmin):

    """
    Класс определяющий интерфейс редактирования Аудио и текста.
    Присутствуют поля для отображения поля фильтрации и поля для поиска.
    Модель AudioAndText.
    """

    list_display = ('title', 'audio_file', 'updated_at')
    list_filter = ('video',)
    search_fields = ('title', 'h1', 'id', 'description')
