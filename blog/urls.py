from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView,PostUpdateView,PostDeleteView,UserPostListView
from . import views
from .views import GameCreateView, GameDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/post-create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('create/', GameCreateView.as_view(), name='game_create'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='play'),

]
