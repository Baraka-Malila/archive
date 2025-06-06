# Generated by Django 5.2.1 on 2025-05-24 17:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("student", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseGroup",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("group_name", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Course Groups",
                "ordering": ["group_name"],
            },
        ),
        migrations.CreateModel(
            name="Courses",
            fields=[
                (
                    "course_code",
                    models.CharField(
                        max_length=5, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("course_name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("credits", models.PositiveIntegerField(default=3)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Courses",
                "ordering": ["course_name"],
            },
        ),
        migrations.CreateModel(
            name="Departments",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Departments",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Assignments",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                ("due_date", models.DateTimeField()),
                ("version", models.CharField(blank=True, max_length=50, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("max_score", models.PositiveIntegerField(default=100)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignments_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignments_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "group_id",
                    models.ForeignKey(
                        blank=True,
                        max_length=50,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resources.coursegroup",
                    ),
                ),
                (
                    "course_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignments",
                        to="resources.courses",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Assignments",
                "ordering": ["due_date"],
            },
        ),
        migrations.CreateModel(
            name="AssignmentSubmissions",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("submission_date", models.DateTimeField(auto_now_add=True)),
                ("score", models.PositiveIntegerField(default=0)),
                ("feedback", models.TextField(blank=True, null=True)),
                ("is_graded", models.BooleanField(default=False)),
                ("attempt_number", models.PositiveIntegerField(default=1)),
                (
                    "file_checksum",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="resources.assignments",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="student.student",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Assignment Submissions",
                "ordering": ["submission_date"],
            },
        ),
        migrations.AddField(
            model_name="coursegroup",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="groups",
                to="resources.courses",
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="department_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="courses",
                to="resources.departments",
            ),
        ),
        migrations.CreateModel(
            name="resources",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("resource_type", models.CharField(max_length=50)),
                ("resource_url", models.URLField(blank=True, null=True)),
                (
                    "resource_file",
                    models.FileField(blank=True, null=True, upload_to="resources/"),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resources",
                        to="resources.assignments",
                    ),
                ),
                (
                    "course_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resources",
                        to="resources.courses",
                    ),
                ),
                (
                    "group_id",
                    models.ForeignKey(
                        blank=True,
                        max_length=50,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resources.coursegroup",
                    ),
                ),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resources_uploaded",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Resources",
                "ordering": ["uploaded_at"],
            },
        ),
    ]
