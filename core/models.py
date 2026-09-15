import re
from urllib.parse import parse_qs, urlparse

from django.core.exceptions import ValidationError
from django.db import models


class Video(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	youtube_url = models.URLField('YouTube URL')
	is_published = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order', '-created_at']

	def __str__(self):
		return self.title

	def clean(self):
		if not self.youtube_id:
			raise ValidationError({'youtube_url': 'Enter a valid YouTube video URL.'})

	@property
	def youtube_id(self):
		parsed = urlparse(self.youtube_url)
		host = parsed.netloc.lower().split(':')[0].removeprefix('www.')
		if host == 'youtu.be':
			candidate = parsed.path.strip('/').split('/')[0]
			return candidate if re.fullmatch(r'[A-Za-z0-9_-]{11}', candidate) else ''
		if host in {'youtube.com', 'm.youtube.com'}:
			if parsed.path == '/watch':
				candidate = parse_qs(parsed.query).get('v', [''])[0]
				return candidate if re.fullmatch(r'[A-Za-z0-9_-]{11}', candidate) else ''
			if parsed.path.startswith(('/embed/', '/shorts/')):
				candidate = parsed.path.split('/')[2]
				return candidate if re.fullmatch(r'[A-Za-z0-9_-]{11}', candidate) else ''
		return ''

	@property
	def youtube_embed_url(self):
		return f'https://www.youtube-nocookie.com/embed/{self.youtube_id}?rel=0'
