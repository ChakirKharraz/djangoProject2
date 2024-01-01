from django import forms
from .models import Game

# Form for creating or updating a game
class GameForm(forms.ModelForm):
    class Meta:
        # Specify the associated model and the fields to include in the form
        model = Game
        fields = ['title', 'grid_size', 'win_size', 'room_code', 'private']

# Form for joining an existing game
class JoinGameForm(forms.Form):
    # Define a password field for joining private games
    password = forms.CharField(widget=forms.PasswordInput, required=False)
