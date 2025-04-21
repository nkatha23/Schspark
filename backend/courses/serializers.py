from rest_framework import serializers
from .models import Course, CourseCategory, CourseEnrollment

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'code', 'icon', 'description']
        read_only_fields = ['id', 'code']

class CourseListSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)
    instructor = serializers.StringRelatedField()
    is_enrolled = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'category', 'instructor',
            'level', 'duration_weeks', 'weekly_hours', 'thumbnail', 'price',
            'enrolled_count', 'capacity', 'is_enrolled', 'availability'
        ]
    
    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(student=request.user, is_active=True).exists()
        return False
    
    def get_availability(self, obj):
        return {
            'available': obj.is_available,
            'seats_left': max(0, obj.capacity - obj.enrolled_count),
            'percent_filled': int((obj.enrolled_count / obj.capacity) * 100) if obj.capacity > 0 else 0
        }

class CourseDetailSerializer(CourseListSerializer):
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    
    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + [
            'description', 'start_date', 'end_date', 'status'
        ]

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    student = serializers.StringRelatedField()
    
    class Meta:
        model = CourseEnrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'completed_at', 'is_active']
        read_only_fields = ['id', 'student', 'course', 'enrolled_at']

class EnrollmentActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['enroll', 'unenroll'])