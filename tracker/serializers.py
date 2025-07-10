# tracker/serializers.py
from rest_framework import serializers
from .models import TreeViewSettings

class TreeViewSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeViewSettings
        fields = ['show_notes', 'notes_count', 'show_stars', 'stars_count']