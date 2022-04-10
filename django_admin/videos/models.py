"""Файл для создания ORM моделей."""
from typing import Any

from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


def create_file_name() -> uuid.UUID:

    """
    Функция для создания уникального имени файла без расширения.

    Returns:
        Вернёт UUID, в качестве имени файла.
    """

    return uuid.uuid4()


def create_path_audio(instance: Any, filename: Any) -> str:

    """
    Функция для создания пути аудио-трека.
    Подробнее см.
    https://docs.djangoproject.com/en/4.0/ref/models/fields/

    Args:
        instance: см. док.
        filename: см. док.

    Returns:
        Вернёт строку (путь) к треку.
    """

    return f'audio/{create_file_name()}'


def create_path_video(instance: Any, filename: Any) -> str:

    """
    Функция для создания пути видео-трека.
    Подробнее см.
    https://docs.djangoproject.com/en/4.0/ref/models/fields/

    Args:
        instance: см. док.
        filename: см. док.

    Returns:
        Вернёт строку (путь) к треку.
    """

    return f'video/{create_file_name()}'


class IdTimeStampedMixin(models.Model):

    """
    Класс-миксин для вставки одинаковых полей в модели.
    Мы будем наследоваться от него,
    тем самым общие поля не придётся прописывать каждый раз сначала,
    что уменьшает объём кодовой базы.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        """
        Мета-класс, нужный для служебной информации.

        Класс IdTimeStampedMixin является абстрактным.
        Т.е. он не будет воспринят Django,
        а нужен нам для личного пользования.
        """

        abstract = True  # Именно про это и сказано выше.


class Langs(IdTimeStampedMixin):

    """Класс ORM модели Langs."""

    full_title = models.CharField(_('Full title'), max_length=50)
    iso_639_1 = models.CharField('ISO 639-1', max_length=10)
    iso_639_2 = models.CharField('ISO 639-2', max_length=10, blank=True)

    class Meta:

        """Мета-класс, нужный для служебной информации."""

        db_table = 'content"."langs'
        verbose_name = _('Lang')
        verbose_name_plural = _('Langs')

    def __str__(self) -> models.CharField:

        """
        Магический метод, для корректного отображения поля в админке.
        Без него Django по умолчанию будет отображать Id, что не очень информативно.

        Returns:
            Вернёт строку, в которой будет красивый текст, для отображения в админке.
        """

        return self.full_title


class VideoTrack(IdTimeStampedMixin):

    """Класс ORM модели VideoTrack."""

    title = models.CharField(_('Video track title'), max_length=65)
    video_file = models.FileField(_('Video track file'), upload_to=create_path_video)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        """Мета-класс, нужный для служебной информации."""

        db_table = 'content"."video_track'
        verbose_name = _('Video track')
        verbose_name_plural = _('Video tracks')

    def __str__(self) -> models.CharField:

        """
        Магический метод, для корректного отображения поля в админке.
        Без него Django по умолчанию будет отображать Id, что не очень информативно.

        Returns:
            Вернёт строку, в которой будет красивый текст, для отображения в админке.
        """

        return self.title


class AudioTrack(IdTimeStampedMixin):

    """Класс ORM модели AudioTrack."""

    title = models.CharField(_('Audio track title'), max_length=65)
    audio_file = models.FileField(_('Audio track file'), upload_to=create_path_audio)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Мета-класс, нужный для служебной информации."""

        db_table = 'content"."audio_track'
        verbose_name = _('Audio track')
        verbose_name_plural = _('Audio tracks')

    def __str__(self) -> models.CharField:
        """
        Магический метод, для корректного отображения поля в админке.
        Без него Django по умолчанию будет отображать Id, что не очень информативно.

        Returns:
            Вернёт строку, в которой будет красивый текст, для отображения в админке.
        """

        return self.title


class Video(IdTimeStampedMixin):

    """Класс ORM модели Video."""

    lang = models.ForeignKey(
        'Langs',
        on_delete=models.CASCADE,
        db_index=False,
        db_column='lang',
        verbose_name=_('Lang')
    )
    video_track = models.ForeignKey(
        'VideoTrack',
        on_delete=models.CASCADE,
        db_index=False,
        verbose_name=_('Video track')
    )
    audio_track = models.ForeignKey(
        'AudioTrack',
        on_delete=models.CASCADE,
        db_index=False,
        verbose_name=_('Audio track')
    )
    title = models.CharField(_('Title'), max_length=50)
    h1 = models.CharField('h1', max_length=50)
    description = models.TextField(_('Description'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        """Мета-класс, нужный для служебной информации."""

        db_table = 'content"."video'
        verbose_name = _('Video')
        verbose_name_plural = _('Video')

    def __str__(self) -> models.CharField:

        """
        Магический метод, для корректного отображения поля в админке.
        Без него Django по умолчанию будет отображать Id, что не очень информативно.

        Returns:
            Вернёт строку, в которой будет красивый текст, для отображения в админке.
        """

        return self.title
