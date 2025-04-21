from django.contrib import admin
from .models import Course, CourseCategory, CourseEnrollment

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')
    search_fields = ('name', 'code')
    list_filter = ('code',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'level', 'status', 'enrolled_count', 'capacity')
    list_filter = ('category', 'level', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('enrolled_count',)

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_active')
    list_filter = ('is_active', 'course')
    search_fields = ('student__username', 'course__title')