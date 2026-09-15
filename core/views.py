from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Video


@login_required
def dashboard(request):
	videos = Video.objects.filter(is_published=True)
	return render(request, 'core/dashboard.html', {'videos': videos})


@login_required
def video_detail(request, pk):
	video = get_object_or_404(Video, pk=pk, is_published=True)
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
