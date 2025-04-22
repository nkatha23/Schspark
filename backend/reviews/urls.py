from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('add', views.add_review, name='add_review'),
    path('<int:id>', views.review_by_id, name='review_by_id'),
    path('<int:progress_id>', views.progress_detail, name='progress_detail'),

    
]
