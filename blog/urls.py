from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views
from .views import GameCreateView, GameDetailView, GameListView, JoinGameView
from .views import update_game_status, store_cell, get_grid_cells, updateDatasP2

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
]
