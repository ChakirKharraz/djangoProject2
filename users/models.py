from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import random
import string


def generate_default_symbol():
    letter = random.choice(string.ascii_uppercase)
    number = random.randint(0, 9)
    return f'{letter}{number}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    symbol = models.CharField(max_length=2, default=generate_default_symbol)
    score = models.IntegerField(default=0)
    game_played = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)