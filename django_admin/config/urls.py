"""
Конфиг URL Конфигурация.
Дополнительные сведения об этом файле см.
https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
]

# Изменение системных переменных Django.
# Тут прописываются все текстовые элементы сайта,
# которые мы хотим переопределить с default, на свои.

admin.site.site_header = 'Консоль управления контентом'
