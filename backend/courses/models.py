from django.db import models

# Create your models here.

# 1. Course Progress Tracking:
#     - Create a model (CourseProgress) to track user progress in a course.
#     - Implement progress updates when a student completes a lesson or module.
# 2. Course Rating & Review:
#     - Set up the CourseReview model for students to rate courses and provide feedback.
#     - Create endpoints for submitting reviews and fetching ratings for courses.

# # Models to be Built
# 1. CourseProgress: to track user progress in a course.

# 2. CourseReview: to allow students to rate courses and provide feedback.

class CourseProgress(models.Model):
    user = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    progress = models.CharField(max_length=255)
    last_updated = models.DateField(auto_now=True)
    progress_percentage = models.IntegerField()

class CourseReview(models.Model):
    rating = models.CharField(max_length=255)
    review = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
