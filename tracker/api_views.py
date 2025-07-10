import logging
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from tracker.models import Classrooms, Students, TreeViewSettings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TreeViewSettingsSerializer

User = get_user_model()

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser)
def api_users(request):
    users = User.objects.all().order_by('id')
    data = [
        {
            'id': u.id, # type: ignore
            'email': u.email,
            'role': getattr(u, 'role', None),
            'is_active': u.is_active,
            'is_superuser': u.is_superuser,
            'date_joined': u.date_joined.isoformat(),
            'email_verified': getattr(u, 'email_verified', None),
            'blocked': getattr(u, 'blocked', None),
        }
        for u in users
    ]
    return JsonResponse(data, safe=False)

@user_passes_test(lambda u: u.is_authenticated)
def api_classes(request):
    classrooms = Classrooms.objects.filter(teacher=request.user).order_by('edited_at')[:6]
    data = [
        {
            'id': c.id,
            'name': c.name,
            'teacher_id': c.teacher.id if c.teacher else None, # type: ignore
            'teacher_username': c.teacher.username if c.teacher else None,
            'teacher_email': c.teacher.email if c.teacher else None,
            'edited_at': c.edited_at.isoformat(),
        }
        for c in classrooms
    ]
    return JsonResponse(data, safe=False)

@user_passes_test(lambda u: u.is_authenticated)
def api_students(request):
    students = Students.objects.filter(classroom__teacher=request.user).order_by('id')
    data = [
        {
            'id': s.id,
            'name': s.name,
            'email': s.email,
            'teacher': s.classroom.teacher.username if s.classroom and s.classroom.teacher else None,
            'classroom_id': s.classroom.id if s.classroom else None,
            'classroom_name': s.classroom.name if s.classroom else None,
            'stars_count': s.stars_count,
        }
        for s in students
    ]
    return JsonResponse(data, safe=False)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def treeview_settings_api(request):
    settings, _ = TreeViewSettings.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = TreeViewSettingsSerializer(settings)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TreeViewSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data})
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increment_star_count(request):
    student = Students.objects.filter(id=request.data.get('student_id')).first()
    logging.info(f"Incrementing star count for student: {student.id if student else 'Not found'}")
    if student:
        student.stars_count += 1
        student.save()
        return Response({'status': 'success', 'stars_count': student.stars_count})
    return Response({'status': 'error', 'message': 'Student not found'}, status=404),


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_star_count(request):
    student = Students.objects.filter(id=request.data.get('student_id')).first()
    logging.info(f"Removing star count for student: {student.id if student else 'Not found'}")
    if student:
        student.stars_count -= 1
        student.save()
        return Response({'status': 'success', 'stars_count': student.stars_count})
    return Response({'status': 'error', 'message': 'Student not found'}, status=404)