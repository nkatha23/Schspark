from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, CourseEnrollment
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    CourseEnrollmentSerializer,
    EnrollmentActionSerializer
)
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Course.objects.filter(status='PUBLISHED').select_related('category', 'instructor')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Course.objects.all()
    lookup_field = 'id'

class EnrollmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, status='PUBLISHED')
        serializer = EnrollmentActionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        action = serializer.validated_data['action']
        
        if action == 'enroll':
            return self.handle_enrollment(request.user, course)
        elif action == 'unenroll':
            return self.handle_unenrollment(request.user, course)
    
    def handle_enrollment(self, user, course):
        if not course.is_available:
            return Response(
                {'detail': 'This course is full or not available for enrollment.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        enrollment, created = CourseEnrollment.objects.get_or_create(
            student=user,
            course=course,
            defaults={'is_active': True}
        )
        
        if not created and enrollment.is_active:
            return Response(
                {'detail': 'You are already enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not created:
            enrollment.is_active = True
            enrollment.save()
        
        self.notify_enrollment_update(course)
        
        return Response(
            {'detail': 'Successfully enrolled in the course.'},
            status=status.HTTP_201_CREATED
        )
    
    def handle_unenrollment(self, user, course):
        try:
            enrollment = CourseEnrollment.objects.get(
                student=user,
                course=course,
                is_active=True
            )
            enrollment.is_active = False
            enrollment.save()
            
            self.notify_enrollment_update(course)
            
            return Response(
                {'detail': 'Successfully unenrolled from the course.'},
                status=status.HTTP_200_OK
            )
        except CourseEnrollment.DoesNotExist:
            return Response(
                {'detail': 'You are not enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def notify_enrollment_update(self, course):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'course_{course.id}',
            {
                'type': 'course_message',
                'message': 'enrollment_updated'
            }
        )

class UserEnrollmentsView(generics.ListAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CourseEnrollment.objects.filter(
            student=self.request.user,
            is_active=True
        ).select_related('course', 'student')



