from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    EnrollmentView,
    UserEnrollmentsView
)
urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('<uuid:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('<uuid:course_id>/enroll/', EnrollmentView.as_view(), name='course-enroll'),
    path('my-enrollments/', UserEnrollmentsView.as_view(), name='user-enrollments'),
]