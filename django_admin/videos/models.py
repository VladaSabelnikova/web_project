"""Файл для создания ORM моделей."""

from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


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


class Video(IdTimeStampedMixin):

    """Класс ORM модели Video."""

    video_file = models.FileField(_('Video file'), upload_to='video/')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        """Мета-класс, нужный для служебной информации."""

        db_table = 'content"."video'
        verbose_name = _('Video')
        verbose_name_plural = _('Video')

    def __str__(self) -> models.FileField:

        """
        Магический метод, для корректного отображения поля в админке.
        Без него Django по умолчанию будет отображать Id, что не очень информативно.

        Returns:
            Вернёт строку, в которой будет красивый текст, для отображения в админке.
        """

        return self.video_file


class AudioAndText(IdTimeStampedMixin):

    """Класс ORM модели AudioAndText."""

    video = models.ForeignKey('Video', on_delete=models.CASCADE, db_index=False)
    audio_file = models.FileField(_('Audio file'), upload_to='audio/')
    title = models.CharField(_('Title'), max_length=50)
    h1 = models.CharField('h1', max_length=50)
    description = models.TextField(_('Description'))
    lang = models.ForeignKey('Langs', on_delete=models.CASCADE, db_index=False, db_column='lang')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        """Мета-класс, нужный для служебной информации."""

        db_table = 'content"."audio_and_text'
        verbose_name = _('Audio and text')
        verbose_name_plural = _('Audio and texts')

    def __str__(self) -> models.CharField:

        """
        Магический метод, для корректного отображения поля в админке.
        Без него Django по умолчанию будет отображать Id, что не очень информативно.

        Returns:
            Вернёт строку, в которой будет красивый текст, для отображения в админке.
        """

        return self.title
