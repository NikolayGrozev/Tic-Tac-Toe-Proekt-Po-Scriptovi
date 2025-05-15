from django.urls import path, include
from app import views

urlpatterns = [
    path('users/', views.get_users, name = 'user_list'),
    path('users/new/', views.create_user, name = 'new_user'),
    path('users/<int:pk>/', views.user, name = 'user_detail'),
]
