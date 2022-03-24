from django.contrib import admin

# Register your models here.
from .models import Langs


@admin.register(Langs)
class LangsAdmin(admin.ModelAdmin):
    pass
