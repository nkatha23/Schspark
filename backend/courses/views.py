from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, CourseEnrollmentSerializer

class TestAPIView(APIView):
    def get(self, request):
        return Response({"message": "API is working!"}, status=status.HTTP_200_OK)

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.filter(status='PUBLISHED')
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

class EnrollmentView(generics.CreateAPIView):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserEnrollmentsView(generics.ListAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseEnrollment.objects.filter(student=self.request.user)
