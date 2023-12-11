from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views
from .views import GameCreateView, GameDetailView, GameListView, JoinGameView
from .views import update_game_status
from .views import get_game_cell,get_game_grid,update_game_cell

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
    path('update_game_cell/', update_game_cell, name='update_game_cell'),
    path('check_for_updates/<int:game_id>/', views.check_for_updates, name='check_for_updates'),
    path('get_game_cell/', get_game_cell, name='get_game_cell'),
    path('get_game_grid/<int:game_id>/', get_game_grid, name='get_game_grid'),

]
