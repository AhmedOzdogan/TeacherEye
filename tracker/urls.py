# File: tracker/urls.py
# This file defines the URL patterns for the tracker app of the TeacherEye project.
from django.urls import path

from tracker.api_views import api_classes, api_users, api_students, increment_star_count, remove_star_count, treeview_settings_api
from . import views

urlpatterns = [
    path('dashboard_teachers/', views.dashboard_teachers, name='dashboard_teachers'),
    path('dashboard_managers/', views.dashboard_managers, name='dashboard_managers'),
    path('dashboard_admins/', views.dashboard_admins, name='dashboard_admins'),
    path('api/users/', api_users),
    path('api/classes/', api_classes),
    path('api/students/', api_students),
    path('class/<int:class_id>/', views.classroom_detail_view, name='classroom_detail'),
    path('api/treeview-settings/', treeview_settings_api),
    path('api/treeview-settings/increment-star/', increment_star_count),
    path('api/treeview-settings/remove-star/', remove_star_count),
]