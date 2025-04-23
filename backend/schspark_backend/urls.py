from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf.urls.static import static
import os
from django.conf import settings
from django.views.generic.base import RedirectView 

@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "Welcome to Schspark API",
        "endpoints": {
            "courses": "/api/courses/",
            "categories": "/api/categories/",
            "reviews": "/api/reviews/",
        }
    })

def home(request):
    return HttpResponse("""
        <html>
        <head>
            <link rel="icon" href="data:,">
            <title>Schspark</title>
        </head>
        <body>
            <h1>Welcome to Schspark API</h1>
            <p>Visit our API at <a href="/api/">/api/</a></p>
        </body>
        </html>
    """, content_type="text/html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_home, name='api-home'),
    path('api/courses/', include('courses.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('', home, name='home'),
   path('favicon.ico', RedirectView.as_view(url='/static/courses/img/favicon.ico', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)