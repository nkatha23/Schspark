
from rest_framework import serializers
from .models import Review, Progress

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review', 'rating', 'course', 'created_at']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'status', 'course', 'progress_percentage', 'last_updated']