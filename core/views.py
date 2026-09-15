from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Video


@login_required
def dashboard(request):
	courses = Course.objects.filter(is_published=True).prefetch_related('videos')
	uncategorized_videos = Video.objects.filter(course__isnull=True, is_published=True)
	return render(request, 'core/dashboard.html', {
		'courses': courses,
		'uncategorized_videos': uncategorized_videos,
	})


@login_required
def course_detail(request, pk):
	course = get_object_or_404(
		Course.objects.prefetch_related('videos'),
		pk=pk,
		is_published=True,
	)
	videos = course.videos.filter(is_published=True)
	return render(request, 'core/course_detail.html', {'course': course, 'videos': videos})


@login_required
def video_detail(request, pk):
	video = get_object_or_404(
		Video,
		Q(course__isnull=True) | Q(course__is_published=True),
		pk=pk,
		is_published=True,
	)
	return render(request, 'core/video_detail.html', {'video': video})


def health(request):
	return JsonResponse({'status': 'ok'})


def signup(request):
	form = UserCreationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = form.save()
		login(request, user)
		return redirect('dashboard')
	return render(request, 'core/signup.html', {'form': form})
