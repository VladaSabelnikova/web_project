from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class IdTimeStampedMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Langs(IdTimeStampedMixin):
    full_title = models.CharField(_('Full title'), max_length=50)
    iso_639_1 = models.CharField('ISO 639-1', max_length=10)
    iso_639_2 = models.CharField('ISO 639-2', max_length=10, blank=True)

    class Meta:
        db_table = 'content"."langs'
        verbose_name = _('Lang')
        verbose_name_plural = _('Langs')

    def __str__(self):
        return self.full_title


class Video(IdTimeStampedMixin):
    path_to_video = models.CharField(_('Path to video'), max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content"."video'
        verbose_name = _('Video')
        verbose_name_plural = _('Video')

    def __str__(self):
        return self.path_to_video


class AudioAndText(IdTimeStampedMixin):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, db_index=False, db_column='video')
    path_to_audio = models.CharField(_('Path to audio'), max_length=255)
    title = models.CharField(_('Title'), max_length=50)
    h1 = models.CharField('h1', max_length=50)
    description = models.TextField(_('Description'))
    lang = models.ForeignKey('Langs', on_delete=models.CASCADE, db_index=False, db_column='lang')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content"."audio_and_text'
        verbose_name = _('Audio and text')
        verbose_name_plural = _('Audio and texts')
        indexes = [
            models.Index(fields=['title'], name='audio_and_text_title_idx'),
            models.Index(fields=['description'], name='audio_and_text_description_idx')
        ]

    def __str__(self):
        return self.title
