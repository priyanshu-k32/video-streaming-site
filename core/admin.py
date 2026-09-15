from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_published', 'order', 'created_at')
	list_filter = ('is_published',)
	search_fields = ('title', 'description')
	list_editable = ('is_published', 'order')
