from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class IdTimeStampedMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Langs(IdTimeStampedMixin):
    full_title = models.CharField(_('full_title'), max_length=50)
    iso_639_1 = models.CharField(_('ISO 639-1'), max_length=10)
    iso_639_2 = models.CharField(_('ISO 639-2'), max_length=10, blank=True)

    class Meta:
        db_table = 'content"."langs'
        verbose_name = _('lang')
        verbose_name_plural = _('langs')

    def __str__(self):
        return self.full_title


class Video(IdTimeStampedMixin):
    path_to_video = models.CharField(_('path_to_video'), max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content"."video'
        verbose_name = _('video')
        verbose_name_plural = _('video')

    def __str__(self):
        return self.path_to_video


class AudioAndText(IdTimeStampedMixin):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, db_index=False, db_column='video')
    path_to_audio = models.CharField(_('path_to_audio'), max_length=255)
    title = models.CharField(_('title'), max_length=50)
    h1 = models.CharField(_('h1'), max_length=50)
    description = models.TextField(_('description'))
    lang = models.ForeignKey('Langs', on_delete=models.CASCADE, db_index=False, db_column='lang')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content"."audio_and_text'
        verbose_name = _('audio_and_text')
        verbose_name_plural = _('audio_and_texts')
        indexes = [
            models.Index(fields=['title'], name='audio_and_text_title_idx'),
            models.Index(fields=['description'], name='audio_and_text_description_idx')
        ]

    def __str__(self):
        return self.title
