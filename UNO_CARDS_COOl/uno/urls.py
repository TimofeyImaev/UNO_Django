from django.urls import path
from . import views
from .game_templates import get_all_logged_in_users_request, Hello_World, ChangePlayerReady
from .views import Get_Cards

urlpatterns = [
    path('cardgame/', views.index, name = 'home'),
    path('register/', views.create_student, name = 'signin'),
    path('api/v1/logout/', views.LogoutView),
    path('game/', views.GameStatus, name = 'game'),
    path('api/v1/info_query/', get_all_logged_in_users_request, name = 'team_query'),
    path('api/v1/change_ready', ChangePlayerReady, name = "ready"),
    path('api/v1/get_cards/', Get_Cards, name = "get_cards"),
    path('api/v1/turn', views.PostTurn, name = "turn"),
    path('api/v1/lobby_query/', views.lobby_query, name = "lobby_query"),
    path('api/v1/join_query', views.join_query, name = "join_query"),
    path('api/v1/get_query', views.get_query, name = "get_query"),
    path('api/v1/join_lobby', views.join_lobby, name = "join_lobby"),
    path('api/v1/join_refuse', views.join_refuse, name = "join_refuse"),
]