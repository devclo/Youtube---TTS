# ytdownloader/admin.py
from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'video_url', 'download_path')
    search_fields = ('title',)
