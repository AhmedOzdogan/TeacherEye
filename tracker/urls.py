# File: tracker/urls.py
# This file defines the URL patterns for the tracker app of the TeacherEye project.
from django.urls import path, include
from tracker.api_views import StudentViewSet, api_classes, api_users, api_students, increment_star_count, remove_star_count, treeview_settings_api
from . import views
from rest_framework.routers import DefaultRouter


# Setting up a router for the StudentViewSet
router = DefaultRouter()    
router.register(r'students', StudentViewSet, basename='students')

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
    path('api/', include(router.urls)),  # Include the router URLs for the StudentViewSet
    path('add-new-class/', views.add_new_class, name='add_new_class'),
]
