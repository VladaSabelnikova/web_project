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
