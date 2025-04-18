from django.contrib import admin
from .models import Course, CourseCategory, CourseEnrollment

# Register your models here.
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CourseEnrollment)
