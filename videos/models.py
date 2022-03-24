from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class IdTimeStampedMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Langs(IdTimeStampedMixin):
    full_title = models.CharField(_('full_title'), max_length=255)
    iso_639_1 = models.CharField(_('ISO 639-1'), max_length=255)
    iso_639_2 = models.CharField(_('ISO 639-2'), max_length=255, blank=True)

    class Meta:
        db_table = 'content"."langs'
        verbose_name = _('lang')
        verbose_name_plural = _('langs')

    def __str__(self):
        return self.full_title
