from django.contrib import admin

# Register your models here.
from .models import Langs, Video, AudioAndText


class AudioAndTextInline(admin.TabularInline):
    model = AudioAndText


@admin.register(Langs)
class LangsAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'iso_639_1', 'created_at',)
    search_fields = ('id', 'full_title', 'iso_639_1', 'iso_639_2')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = (AudioAndTextInline,)
    list_display = ('path_to_video', 'updated_at')
    search_fields = ('id',)


@admin.register(AudioAndText)
class AudioAndTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'path_to_audio', 'updated_at')
    list_filter = ('video',)
    search_fields = ('title', 'h1', 'id', 'description')
