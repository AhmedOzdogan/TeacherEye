import logging
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from tracker.models import Classrooms, Students, TreeViewSettings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import StudentSerializer, TreeViewSettingsSerializer, ClassroomSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework import viewsets


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

@api_view(['GET', 'POST'])
@user_passes_test(lambda u: u.is_authenticated) # type: ignore
def api_classes(request):
    if request.method == "GET":
        classrooms = Classrooms.objects.filter(teacher=request.user).order_by('edited_at')[:6]
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # Handle CREATE (no ID expected)
        serializer = ClassroomSerializer(data=request.data)
        print("Received POST data for classroom:", request.data)
        if serializer.is_valid():
            classroom = serializer.save(teacher=request.user)
            return Response({'id': classroom.id, 'name': classroom.name}, status=status.HTTP_201_CREATED)  # type: ignore
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'POST'])
@user_passes_test(lambda u: u.is_authenticated)  # type: ignore
def api_students(request):
    if request.method == 'GET':
        students = Students.objects.filter(classroom__teacher=request.user).order_by('id')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        logging.info(f"Received data for students: {data}")

        # Check if this is a bulk post
        is_bulk = isinstance(data, list)

        serializer = StudentSerializer(data=data, many=is_bulk)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': 'success', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )

        print("Student serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Students.objects.filter(classroom__teacher=self.request.user)