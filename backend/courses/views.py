from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, CourseEnrollmentSerializer


class TestAPIView(APIView):
    """Test endpoint to verify API functionality"""
    def get(self, request):
        return Response(
            {"message": "API is working!"}, 
            status=status.HTTP_200_OK
        )


class CourseListView(generics.ListAPIView):
    """List all available courses"""
    queryset = Course.objects.filter(status='PUBLISHED')
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class CourseDetailView(generics.RetrieveAPIView):
    """Retrieve a single course detail"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


class EnrollmentView(generics.CreateAPIView):
    """Handle course enrollments"""
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserEnrollmentsView(generics.ListAPIView):
    """List enrollments for current user"""
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseEnrollment.objects.filter(
            student=self.request.user
        )