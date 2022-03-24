from django.contrib import admin

# Register your models here.
from .models import Langs, Video, AudioAndText


@admin.register(Langs)
class LangsAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(AudioAndText)
class AudioAndTextAdmin(admin.ModelAdmin):
    pass
