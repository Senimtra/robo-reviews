from django.http import HttpResponse
from django.shortcuts import render

# Import functions to handle business logic
from .functions import top_games_images, count_ratings_games, top_combat_picks, summarize_reviews
from .models import Review


# Main index view to display game-related information
def index(request):
    # Fetch top combat game picks for display
    top_combat_game_picks = top_combat_picks()
    # Extract the titles of the top combat games for summarization
    summ_games = [game['title'] for game in top_combat_game_picks]
    # Generate blog-style summaries for the top games
    summarized_text = summarize_reviews(summ_games)
    # Fetch the list of images for the top-rated games
    top_games_image_list = top_games_images()
    # Fetch game and review counts categorized by genre
    db_count_ratings_games = count_ratings_games()
    # Prepare context data to send to the template
    context = {
        'top_games_image_list': top_games_image_list,  # List of images for the top games
        'genre_all_games': db_count_ratings_games[0],  # Game counts by genre
        'genre_all_reviews': db_count_ratings_games[1],  # Review counts by genre
        'top_combat_picks': top_combat_game_picks,  # Details of top combat games
        'summarized_text': summarized_text  # Summarized blog content
    }
    
    # Render the 'index.html' template with the provided context
    return render(request, 'index.html', context)


# Detail view for a specific game
def detail(request, parent_asin):
    # Return a simple HTTP response displaying the game's parent ASIN
    return HttpResponse("You're looking at game %s." % parent_asin)

# Reviews view for a specific game
def reviews(request, parent_asin):
    # Return a simple HTTP response displaying reviews for the game
    response = "You're looking at the reviews for game %s."
    return HttpResponse(response % parent_asin)

# Genre view for a specific game
def genre(request, parent_asin):
    # Return a simple HTTP response displaying the game's genre
    return HttpResponse("You're looking at the genre of game %s." % parent_asin)
