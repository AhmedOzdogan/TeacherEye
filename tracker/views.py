import logging
from django.shortcuts import get_object_or_404, render
from core.decorators import manager_required, admin_required
from .models import Classrooms, Students, TreeViewSettings


def dashboard_teachers(request):
    """
    Render the teacher's dashboard.
    """
    # For now, just render a simple template
    return render(request, 'tracker/dashboard_teachers.html', {'current_user': request.user})

@manager_required
def dashboard_managers(request):
    """
    Render the manager's dashboard.
    """
    # For now, just render a simple template
    return render(request, 'tracker/dashboard_managers.html')

@admin_required
def dashboard_admins(request):

    return render(request, 'tracker/dashboard_admins.html')

def classroom_detail_view(request, class_id):
    classroom = get_object_or_404(Classrooms, id=class_id)
    settings, _ = TreeViewSettings.objects.get_or_create(user=request.user)
    note_range = list(range(0, 6))
    return render(request, 'tracker/classroom_detail.html', {'classroom': classroom , 'settings': settings, 'note_range': note_range})

def add_new_class(request):
    """
    Render the form to add a new class.
    """
    if request.method == 'POST':
        # Handle form submission logic here
        pass
    return render(request, 'tracker/add_new_class.html', {'current_user': request.user})