from django.urls import path
from .views import (
    TestAPIView,
    CourseListView,
    CourseDetailView,
    EnrollmentView,        # Existing view
    UserEnrollmentsView    # Existing view
)

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='api-test'),
    path('', CourseListView.as_view(), name='course-list'),
    path('<uuid:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('enroll/', EnrollmentView.as_view(), name='enroll'),  # Changed path
    path('my-enrollments/', UserEnrollmentsView.as_view(), name='user-enrollments'),
]