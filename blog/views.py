from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView, View
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Game
from .forms import GameForm,JoinGameForm
from django.urls import reverse_lazy
from django.contrib import messages

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False



class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'blog/create_game.html'

    def form_valid(self, form):
        form.instance.game_author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('play-game', kwargs={'pk': self.object.id})

class GameDetailView(DetailView):
    model = Game
    template_name = 'blog/play.html'


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'blog/game_list.html'
    context_object_name = 'games'
    ordering = ['-date_posted']

    def get_queryset(self):
        # Exclude finished games from the queryset
        return Game.objects.filter(finished=False).order_by('-date_posted')

class JoinGameView(LoginRequiredMixin, View):
    template_name = 'blog/join_game.html'
    form_class = JoinGameForm
    model = Game

    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        if game and not game.finished:
            # Only include the password field if the game has a password
            form = self.form_class() if game.room_code else None
            return render(request, self.template_name, {'form': form, 'game_id': game_id, 'game': game})
        else:
            messages.error(request, 'Cette partie n\'existe pas ou est terminée.')
            return redirect('game-list')

    def post(self, request, game_id):
        form = self.form_class(request.POST)
        game = get_object_or_404(Game, id=game_id)

        if form.is_valid():
            entered_password = form.cleaned_data['password']

            if not game.room_code and not entered_password:
                # Si la partie n'a pas de mot de passe, et aucun mot de passe n'est entré, rejoindre automatiquement
                return self.join_game(game)
            elif entered_password == game.room_code:
                return self.join_game(game)
            else:
                messages.error(request, 'Mot de passe incorrect.')
        else:
            messages.error(request, 'Formulaire invalide. Veuillez réessayer.')

        return render(request, self.template_name, {'form': form, 'game_id': game_id, 'game': game})

    def join_game(self, game):
        if not game.finished:
            if not game.game_player2 and self.request.user != game.game_author:
                game.game_player2 = self.request.user
                game.save()
                return redirect('play-game', pk=game.id)
            elif game.game_player2 or self.request.user == game.game_author:
                return redirect('play-game', pk=game.id)
        else:
            return redirect('play-game', pk=game.id)

        messages.error(self.request, 'Vous ne pouvez pas rejoindre cette partie.')
        return redirect('game-list')
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
