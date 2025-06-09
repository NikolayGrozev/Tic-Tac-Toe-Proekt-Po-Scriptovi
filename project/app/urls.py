from django.urls import path, include
from app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/', views.get_users, name = 'user_list'),
    path('users/new/', views.create_user, name = 'new_user'),
    path('users/<int:pk>/', views.user, name = 'user_detail'),
    path("friend-requests/", views.get_friend_requests, name = 'friend_requests'),
    path("friend-requests/send/<int:pk_sent_to>/", views.send_friend_request, name='send_friend_request'),
    path("friend-requests/respond/<int:pk_frequest>/", views.respond_friend_request, name='respond_friend_request'),
    path('users/<int:user_pk>/remove-friend/<int:friend_pk>/', views.remove_friend, name = 'unfriend'),
    path('users/<int:pk>/games', views.get_user_games, name = 'games'),
    path('users/create-game/playerX=<int:pk_player_x>/playerO=<int:pk_player_o>', views.create_game, name='create game'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
