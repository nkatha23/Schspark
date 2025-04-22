from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "Welcome to Schspark API",
        "endpoints": {
            "courses": "/api/courses/",
            "categories": "/api/categories/",
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_home, name='api-home'),
    path('courses/', include('courses.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('reviews/', include('reviews.urls')), 

]