# Generated by Django 4.2.6 on 2023-11-18 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_game_alignement_game_grid_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='alignement',
            new_name='win_size',
        ),
    ]
