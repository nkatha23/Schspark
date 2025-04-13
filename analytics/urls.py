from django.urls import path, include 
from rest_framework.routers import DefaultRouter 
from .views import UserActivityViewSet, SystemPerformanceViewSet, LogUserActivityView, ActivitySummaryView
from . import views


router = DefaultRouter()
router.register(r'user-activities', UserActivityViewSet, basename='user-activities')    

router = DefaultRouter()
router.register(r'system-performance', SystemPerformanceViewSet, basename='system-performance')

router = DefaultRouter()
router.register(r'log-user-activities', LogUserActivityView, basename='log-user-activities')

router = DefaultRouter()
router.register(r'activity-summary', ActivitySummaryView, basename='activity-summary')

urlpatterns = [
    path('', include(router.urls)),
    path('user-activities/', UserActivityViewSet.as_view({'get': 'list'}), name='user-activities'),
    path('system-performance/', SystemPerformanceViewSet.as_view({'get': 'list'}), name='system-performance'),
    path('log/', LogUserActivityView.as_view(), name='log-user-activities'),  # Corrected this line
    path('activity-summary/', ActivitySummaryView.as_view({'get': 'list'}), name='activity-summary'),  # Corrected this line
    path('home/', views.home_view, name='home'),  # Added this line for the home view
]