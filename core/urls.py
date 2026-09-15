from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('videos/<int:pk>/', views.video_detail, name='video_detail'),
    path('health/', views.health, name='health'),
]