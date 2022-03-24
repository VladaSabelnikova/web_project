from django.contrib import admin

# Register your models here.
from .models import Langs, Video


@admin.register(Langs)
class LangsAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass
