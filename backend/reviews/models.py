from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


def percentage_validator(value):
    if value < 0 or value > 100:
        raise ValidationError('Progress percentage must be between 0 and 100.')

class Progress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('course_module.Course', on_delete=models.CASCADE)  # Assuming 'course_module' is where the Course model is defined
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_started')
    progress_percentage = models.PositiveIntegerField(validators=[percentage_validator])
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Progress for {self.course.name} by {self.user.username}: {self.status} ({self.progress_percentage}%)"

class Review(models.Model):
    review = models.TextField()
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.rating}/5"
    
