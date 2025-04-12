from rest_framework.viewsets import ViewSet
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserActivity, SystemPerformance
from .serializers import UserActivitySerializer, SystemPerformanceSerializer, ActivitySummarySerializer, LogUserActivitySerializer
from django.db.models import Count


# Create your views here.
class SystemPerformanceViewSet(viewsets.ModelViewSet):
    queryset = SystemPerformance.objects.all()
    serializer_class = SystemPerformanceSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view


class LogUserActivityView(generics.CreateAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActivitySummaryView(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        summary = UserActivity.objects.values('user__username').annotate(total=Count('id'))
        return Response(summary)

# This view will be used to display the home page of the analytics dashboard.
def home_view(request):
    return HttpResponse("Welcome to the Analytics Dashboard!")