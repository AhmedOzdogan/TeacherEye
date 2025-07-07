# File: core/urls.py
# This file defines the URL patterns for the core app of the TeacherEye project.
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('features/', views.features, name='features'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]