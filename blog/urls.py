from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views
from .views import GameCreateView, GameDetailView, GameListView, JoinGameView, StatsView, CustomStatsView
from .views import (update_game_status, store_cell, get_grid_cells, updateDatasP2, switch_turn, get_user, get_symbol,
                    check_game_status, update_current_turn, get_game_statistics)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/post-create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('create/', GameCreateView.as_view(), name='game-create'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='play-game'),
    path('list/', GameListView.as_view(), name='game-list'),
    path('game/join/<int:game_id>/', JoinGameView.as_view(), name='join-game'),
    path('update_game_status/<int:game_id>/', update_game_status, name='update_game_status'),
    path('store_cell/', store_cell, name='store_cell'),
    path('get_grid_cells/<int:game_id>/', get_grid_cells, name='get_grid_cells'),
    path('updateDatasPlayer2/<int:game_id>/', updateDatasP2, name='updateDatasPlayer2'),
    path('switch_turn/<int:game_id>/', switch_turn, name='switch-turn'),
    path('get_user/<int:game_id>/', get_user, name='get_user'),
    path('get_symbol/<int:game_id>/', get_symbol, name='get_symbol'),
    path('check_game_status/<int:game_id>/', check_game_status, name='check_game_status'),
    path('update_current_turn/<int:game_id>/', update_current_turn, name='update_current_turn'),
    path('stats/', StatsView, name='stats'),
    path('get_game_statistics/', get_game_statistics, name='get_game_statistics'),
    path('custom-stats/', CustomStatsView.as_view(), name='custom-stats'),

]
