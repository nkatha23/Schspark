from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

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

   

class CourseCategory(models.Model):
    CATEGORY_CHOICES = [
        ('SEIP', 'Special Education and Inclusive Practices'),
        ('AI', 'Artificial Intelligence'),
        ('CMSE', 'Classroom Management and Student Engagement'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, choices=CATEGORY_CHOICES, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_code_display()} ({self.code})"

    class Meta:
        verbose_name_plural = "Course Categories"
        ordering = ['name']

class Course(models.Model):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=160)
    category = models.ForeignKey(CourseCategory, on_delete=models.PROTECT, related_name='courses')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taught_courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='BEGINNER')
    duration_weeks = models.PositiveIntegerField(default=4)
    weekly_hours = models.PositiveIntegerField(default=2)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    capacity = models.PositiveIntegerField(default=30)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enrolled_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{str(self.id)[:8]}")
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        return self.status == 'PUBLISHED' and self.enrolled_count < self.capacity

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]

class CourseEnrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.student.email} in {self.course.title}"

@receiver(post_save, sender=CourseEnrollment)
def update_enrollment_count(sender, instance, created, **kwargs):
    if created or 'is_active' in instance.get_deferred_fields():
        course = instance.course
        course.enrolled_count = course.enrollments.filter(is_active=True).count()
        course.save()