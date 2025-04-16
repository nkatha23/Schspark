"""
URL configuration for my_schspark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sch_spark import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('sch_spark.urls')),

    path('accounts/', include('allauth.urls')),

    path('dashboard/', views.dashboard, name='dashboard')  # Note the slash at the end

]
