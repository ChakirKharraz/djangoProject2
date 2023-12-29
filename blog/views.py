from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Game, GridCell
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import GameForm, JoinGameForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from users.models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone


def home(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        message = ""
        if self.request.session['game_id']:
            if self.request.session['game_id'] is not None and self.request.session['game_id'] != "":

                game = Game.objects.get(id=self.request.session['game_id'])
                if game.abandonned:
                    if game.winner == self.request.user:
                        message = "YOU WON! Your opponent just gave up"
                    else:
                        message = "You gave up your last game!"


        messages.success(self.request, message)
        self.request.session['game_id'] = ""

        # Add the message to the context
        context['game_message'] = message

        return context


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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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
        # Set the game author to the current user
        form.instance.game_author = self.request.user

        # Check if grid_size is between 3 and 12
        grid_size = form.cleaned_data['grid_size']
        if grid_size < 3 or grid_size > 12:
            messages.error(self.request, 'Please choose a grid size between 3 and 12.')
            return self.form_invalid(form)

        # Check if win_size is between 3 and grid_size
        win_size = form.cleaned_data['win_size']
        if win_size < 3 or win_size > grid_size:
            messages.error(self.request, 'Please choose a win size between 3 and the selected grid size.')
            return self.form_invalid(form)

        form.instance.currentTurn = self.request.user
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


def update_game_status(request, game_id):
    try:
        winning_symbol = request.GET.get('winningSymbol')
        game = Game.objects.get(pk=game_id)

        if not game.finished:
            # Set the finished attribute to True
            game.finished = True

            # Determine the winner and update the winner attribute
            if winning_symbol == game.game_author.profile.symbol:
                game.winner = game.game_author
            elif winning_symbol == game.game_player2.profile.symbol:
                game.winner = game.game_player2

            game.save()

            # Update player profiles
            author_profile = game.game_author.profile  # Access profile through user.profile
            player2_profile = game.game_player2.profile  # Access profile through user.profile

            if game.winner:
                # Increment game_played for both players
                author_profile.game_played += 1
                player2_profile.game_played += 1

                # Update scores based on the game outcome
                if game.winner == game.game_author:
                    author_profile.score += 1
                elif game.winner == game.game_player2:
                    player2_profile.score += 1
            else:
                # In case of a draw, increment game_played for both players
                author_profile.game_played += 1
                player2_profile.game_played += 1
                # No score update for a draw

            author_profile.save()
            player2_profile.save()

            return JsonResponse({'message': 'Game finished successfully'})
        else:
            return JsonResponse({'message': 'Game already finished'})
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found for one or both players'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def store_cell(request):
    if request.method == 'POST':
        try:
            game_id = request.POST.get('game_id')
            row = request.POST.get('row')
            col = request.POST.get('col')
            symbol = request.POST.get('symbol')

            game = get_object_or_404(Game, id=game_id)

            # Store the cell information in the database
            grid_cell = GridCell.objects.create(game=game, row=row, col=col, symbol=symbol)

            game.currentTurn = game.game_author if game.currentTurn == game.game_player2 else game.game_player2
            game.save()

            return JsonResponse({'success': True})
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_grid_cells(request, game_id):
    grid_cells = GridCell.objects.filter(game_id=game_id).values('row', 'col', 'symbol')
    return JsonResponse({'success': True, 'grid_cells': list(grid_cells)})


def updateDatasP2(request, game_id):
    request.session['game_id'] = game_id
    game = get_object_or_404(Game, id=game_id)

    if game.game_player2 == None:
        player2 = "None"
    else:
        player2 = game.game_player2.username

    return JsonResponse({'success': True, 'player2': player2})


def switch_turn(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)

        print(f"Before switching: currentTurn={game.currentTurn}")
        if game.currentTurn.username == game.game_author.username:
            game.currentTurn = game.game_player2
            currentSymbol = game.game_player2.profile.symbol

        else:
            game.currentTurn = game.game_author
            currentSymbol = game.game_author.profile.symbol

        currentUser = game.currentTurn.username;

        print(f"After switching: CURRENT SYMBOL={currentSymbol}")
        print(f"After switching: currentTurn={game.currentTurn}")
        game.save()
        print(f"After saving: currentTurn={game.currentTurn}")

        return JsonResponse(
            {'message': 'Turn switched successfully', 'currentSymbol': currentSymbol, 'currentUser': currentUser})
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_user(request, game_id):
    game = Game.objects.get(pk=game_id)
    currentUser = game.currentTurn.username

    return JsonResponse({'currentUser': currentUser})


def get_symbol(request, game_id):
    game = Game.objects.get(pk=game_id)
    currentSymbol = game.currentTurn.profile.symbol

    return JsonResponse({'currentSymbol': currentSymbol})


def check_game_status(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game_data = {
        'gameFinished': game.finished,
        'winningSymbol': game.winner.profile.symbol if game.finished and game.winner and game.winner.profile else None,
    }
    return JsonResponse(game_data)


def update_current_turn(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    current_turn = game.currentTurn.username if game.currentTurn else None
    return JsonResponse({'currentTurn': current_turn})


class StatsView(LoginRequiredMixin, View):
    template_name = 'blog/stats.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def get_game_statistics(request):
    # Récupérer la date de création du compte de l'utilisateur
    user_creation_date = request.user.date_joined.date()

    # Récupérer la date actuelle
    current_date = timezone.now().date()

    # Générer la liste de toutes les dates entre la date de création et la date actuelle
    all_dates = [user_creation_date + timedelta(days=i) for i in range((current_date - user_creation_date).days + 1)]

    # Récupérer les données de jeu
    games = Game.objects.filter(
        Q(game_author=request.user) | Q(game_player2=request.user),
        finished=True,  # Condition pour inclure uniquement les parties terminées
        date_posted__gte=user_creation_date  # Condition pour inclure les parties après la création du compte
    )

    # Agréger les données par date
    games_by_date = games.annotate(date=TruncDate('date_posted')).values('date').annotate(count=Count('id'))
    games_by_date_dict = {entry['date']: entry['count'] for entry in games_by_date}

    # Remplir les données pour toutes les dates (y compris celles sans parties jouées)
    games_played = [games_by_date_dict.get(date, 0) for date in all_dates]

    return JsonResponse({'dates': all_dates, 'games_played': games_played})


class CustomStatsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Get the values for win_size and grid_size from the request
        win_size = int(request.GET.get('win_size', 3))
        grid_size = int(request.GET.get('grid_size', 3))

        # Ensure that win_size and grid_size are within the specified range
        win_size = max(3, min(win_size, 12))
        grid_size = max(3, min(grid_size, 12))

        # Filter games based on win_size and grid_size
        games = Game.objects.filter(win_size=win_size, grid_size=grid_size, finished=True)

        # Create a dictionary to store user scores
        user_scores = {}

        # Get the current user's username
        current_user_username = self.request.user.username

        # Iterate over the filtered games
        for game in games:
            # Check if there is a winner
            if game.winner:
                # Increment the score for the winner
                user_scores[game.winner.username] = user_scores.get(game.winner.username, 0) + 1

        # Sort the user_scores dictionary by score in descending order
        sorted_user_scores = dict(sorted(user_scores.items(), key=lambda item: item[1], reverse=True))

        return JsonResponse({'success': True, 'user_scores': sorted_user_scores, 'current_user': current_user_username})

    def post(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


class GlobalRankingsView(LoginRequiredMixin, View):
    template_name = 'blog/global_rankings.html'

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all().order_by('-score')
        current_user_username = self.request.user.username

        # Serialize profiles for JSON response
        serialized_profiles = [
            {'user__username': profile.user.username, 'score': profile.score}
            for profile in profiles
        ]

        context = {
            'success': True,
            'profiles': serialized_profiles,
            'current_user': current_user_username
        }

        return JsonResponse(context)


def get_second_player_symbol(request):
    if request.method == 'GET':
        game_id = request.GET.get('gameId')
        game = get_object_or_404(Game, id=game_id)  # Replace with the actual model name

        # Assuming your game_player2 has a profile attribute
        game.abandonned = True
        game.save()

        second_player_symbol = game.game_player2.profile.symbol

        return JsonResponse({'symbol': second_player_symbol})

    return JsonResponse({'error': 'Invalid request'})


def about(request):
    return render(request, 'blog/stats.html', {'title': 'About'})
