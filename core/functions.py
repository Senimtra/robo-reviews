from django.db.models import Avg
from .models import Game

def top_games_images():
    top_games = Game.objects.annotate(avg_rating = Avg(
        'review__rating')).order_by('-avg_rating').values('images')[:55]
    top_game_covers = [0, 2, 3, 4, 5, 8, 9, 10, 13, 14, 18, 19, 22, 
                       23, 27, 28, 33, 37, 39, 41, 46, 47, 49, 54]
    top_games = [game['images'] for i, game in enumerate(top_games) if i in top_game_covers]
    return(top_games)
