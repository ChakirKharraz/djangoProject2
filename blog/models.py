from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Game(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    game_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_player1')
    game_player2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='game_player2')
    finished = models.BooleanField(default=False)
    room_code = models.CharField(max_length=100, null=True, blank=True)
    grid_size = models.PositiveIntegerField(default=3)
    win_size = models.PositiveIntegerField(default=3)
    private = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('play', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        # Ensure grid_size is between 3 and 12
        self.grid_size = max(3, min(self.grid_size, 12))

        # Ensure win_size is between 3 and grid_size
        self.win_size = max(3, min(self.win_size, self.grid_size))

        # Check if game_player2 is not set, and a different user is joining
        if not self.game_player2 and self.game_author != self.game_player2:
            self.game_player2 = self.game_player2

            super().save(*args, **kwargs)

        def set_winner(self, winner):
            self.winner = winner
            self.finished = True
            self.save()
