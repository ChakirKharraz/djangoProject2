from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'grid_size', 'win_size', 'room_code', 'private']


class JoinGameForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
