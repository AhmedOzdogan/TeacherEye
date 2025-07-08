from django.shortcuts import render
from core.decorators import manager_required, admin_required

def dashboard_teachers(request):
    """
    Render the teacher's dashboard.
    """
    # For now, just render a simple template
    return render(request, 'tracker/dashboard_teachers.html')

@manager_required
def dashboard_managers(request):
    """
    Render the manager's dashboard.
    """
    # For now, just render a simple template
    return render(request, 'tracker/dashboard_managers.html')

@admin_required
def dashboard_admins(request):
    """
    Render the admin's dashboard.
    """
    # For now, just render a simple template
    return render(request, 'tracker/dashboard_admins.html')