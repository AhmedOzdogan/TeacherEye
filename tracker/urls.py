# File: tracker/urls.py
# This file defines the URL patterns for the tracker app of the TeacherEye project.
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_teachers/', views.dashboard_teachers, name='dashboard_teachers'),
    path('dashboard_managers/', views.dashboard_managers, name='dashboard_managers'),
    path('dashboard_admins/', views.dashboard_admins, name='dashboard_admins'),
]