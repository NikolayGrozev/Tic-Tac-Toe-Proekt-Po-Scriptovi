from django.urls import path, include
from app import views

urlpatterns = [
    path('users/', views.get_users, name = 'user_list'),
    path('users/new/', views.create_user, name = 'new_user'),
    path('users/<int:pk>/', views.user, name = 'user_detail'),
    path('users/<int:user_pk>/add-friend/<int:friend_pk>/', views.add_friend, name='add_friend'),
    path('users/<int:user_pk>/remove-friend/<int:friend_pk>/', views.remove_friend, name = 'unfriend')
]
