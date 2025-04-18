from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)    # e.g., 'login', 'logout', 'course_view'
    timestamp = models.DateTimeField(auto_now_add=True)
    page_visited = models.CharField(max_length=255, blank=True, null=True)  # e.g., 'course_page', 'profile_page'

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'


    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"


class SystemPerformance(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField()  # Percentage
    memory_usage = models.FloatField(default=0.0)  # Percentage
    disk_usage = models.FloatField()  # Percentage

    class Meta:
        verbose_name = 'System Performance'
        verbose_name_plural = 'System Performances'

    def __str__(self):
        return f"Performance at {self.timestamp} - CPU: {self.cpu_usage}%, Memory: {self.memory_usage}%, Disk: {self.disk_usage}%"


class LogUserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

class ActivitySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)  # e.g., 'login', 'logout', 'course_view'
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Activity Summary'
        verbose_name_plural = 'Activity Summaries'

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"
    


