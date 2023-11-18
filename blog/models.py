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
    game_author = models.ForeignKey(User, on_delete=models.CASCADE)
    game_player2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='game_player2')
    finished = models.BooleanField(default=False)
    room_code = models.CharField(max_length=100)
    grid_size = models.PositiveIntegerField(default=3)
    win_size = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.title
