# Generated by Django 4.2.6 on 2023-11-19 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_game_game_player2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_player1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='room_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
