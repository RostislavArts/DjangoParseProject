# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.videocard_list, name='videocard_list'),
    path('videocard/<int:id>/', views.videocard_detail, name='videocard_detail'),
]
