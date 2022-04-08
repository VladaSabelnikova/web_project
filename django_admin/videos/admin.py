"""Файл для создания админки."""

from django.contrib import admin

from .models import Langs, Video, AudioAndText  # noqa: WPS300


class AudioAndTextInline(admin.StackedInline):
    """
    Класс для вставки аудио и текста со страницы редактирования видео.
    Модель AudioAndText.
    """

    model = AudioAndText

    def get_extra(self, request, obj=None, **kwargs):

        """
        Штука определяет кол-во добавляемых инлайнов.
        Подробнее см.
        https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin.get_extra

        Args:
            request: см. док.
            obj: см. док.
            **kwargs: см. док.

        Returns:
            Возвращает кол-во инлайнов.
        """

        extra = 1
        return extra


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
