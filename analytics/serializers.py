from rest_framework import serializers
from .models import UserActivity, SystemPerformance, LogUserActivity, ActivitySummary
from django.contrib.auth.models import User

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity 
        fields = '__all__'


class SystemPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPerformance
        fields = '__all__'


class LogUserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogUserActivity
        fields = '__all__'


class ActivitySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['user', 'activity_type', 'timestamp']  # Adjust fields as necessary