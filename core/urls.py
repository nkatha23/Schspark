from django.contrib import admin
from django.urls import path, include 
from analytics.views import home_view    # Import the view for the home page

urlpatterns = [
    path('', home_view),    # Set it as the root path
    path('admin/', admin.site.urls),
    path('api/analytics/', include('analytics.urls')),  # Include the analytics app URLs
]
