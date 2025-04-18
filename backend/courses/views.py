from django.shortcuts import renderfrom rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course
from .serializers import CourseSerializer

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)



