from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_instructor(self, obj):
        return {
            'name': f"{obj.instructor.first_name} {obj.instructor.last_name}",
            'avatar': f"https://ui-avatars.com/api/?name={obj.instructor.first_name}+{obj.instructor.last_name}"
        }
