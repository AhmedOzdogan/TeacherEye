from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models import JSONField

User = get_user_model()

class Classrooms(models.Model):
    """
    Model representing a classroom.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    school = models.CharField(max_length=100, blank=True, null=True)

    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='classrooms'
    )
    edited_at = models.DateTimeField(auto_now=True)
    
    notes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Students(models.Model):
    """
    Model representing a student.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    classroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE, related_name='students')
    stars_count = models.PositiveIntegerField(default=0)
    notes = models.JSONField(default=list, blank=True)
    note_overall = models.IntegerField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if isinstance(self.notes, list):
            valid_notes = [n for n in self.notes if isinstance(n, (int, float))]
            self.note_overall = sum(valid_notes) // len(valid_notes) if valid_notes else None
        else:
            self.note_overall = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"
    
class TreeViewSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='treeview_settings')

    show_notes = models.BooleanField(default=False)
    
    show_stars = models.BooleanField(default=False)
    # Add more flags as needed

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s tree view settings"