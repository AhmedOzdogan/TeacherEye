# Generated by Django 3.1.12 on 2025-07-10 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20250710_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classrooms',
            name='slug_name',
        ),
        migrations.RemoveField(
            model_name='classrooms',
            name='slug_school',
        ),
    ]
