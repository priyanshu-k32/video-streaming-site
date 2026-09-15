from django.contrib import admin

from .models import Course, Video


class VideoInline(admin.TabularInline):
	model = Video
	extra = 1
	fields = ('title', 'youtube_url', 'description', 'is_published', 'order')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_published', 'order', 'created_at')
	list_filter = ('is_published',)
	search_fields = ('title', 'description')
	list_editable = ('is_published', 'order')
	inlines = (VideoInline,)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
	list_display = ('title', 'course', 'is_published', 'order', 'created_at')
	list_filter = ('is_published',)
	search_fields = ('title', 'description', 'course__title')
	list_editable = ('is_published', 'order')
