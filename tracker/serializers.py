# tracker/serializers.py
from rest_framework import serializers
from .models import TreeViewSettings, Classrooms , Students

class TreeViewSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeViewSettings
        fields = ['show_notes', 'show_stars']

class ClassroomSerializer(serializers.ModelSerializer):
    teacher_id = serializers.IntegerField(source='teacher.id', read_only=True)
    teacher_username = serializers.CharField(source='teacher.username', read_only=True)
    teacher_email = serializers.EmailField(source='teacher.email', read_only=True)

    class Meta:
        model = Classrooms
        fields = ['id', 'name', 'teacher_id', 'teacher_username', 'teacher_email', 'edited_at', 'notes_count']
        read_only_fields = ['id']

class StudentSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=Classrooms.objects.all(), write_only=True
    )
    classroom_id = serializers.IntegerField(source='classroom.id', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)

    class Meta:
        model = Students
        fields = [
            'id', 'name', 'surname', 'email',
            'classroom',           # for writing
            'classroom_id',        # for reading
            'classroom_name',
            'stars_count', 'notes', 'note_overall'
        ]
