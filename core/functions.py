from django.db.models import Avg, Count, Sum, F
from django.db.models.functions import Substr
from .models import Game, Genre

import openai
import os

# Load the OpenAI API key from the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()


# Function to fetch images of top-rated games
def top_games_images():
    # Annotate games with their average rating, order by rating in descending order, and fetch the top 55
    top_games = Game.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating').values('images')[:55]
    # Specific indices of games to select covers for
    top_game_covers = [0, 2, 3, 4, 5, 8, 9, 10, 13, 14, 18, 19, 22, 
                       23, 27, 28, 33, 37, 39, 41, 46, 47, 49, 54]
    # Filter the games based on the predefined indices
    top_games = [game['images'] for i, game in enumerate(top_games) if i in top_game_covers]
    return top_games


# Function to count games and reviews by genre
def count_ratings_games():
    # Annotate genres with the count of games
    genres_game_count = Genre.objects.values('genre').annotate(game_count=Count('game'))
    # Annotate genres with the count of reviews
    genres_reviews_count = Genre.objects.values('genre').annotate(review_count=Count('game__review'))
    # Create a dictionary for game counts
    games_count = {''.join(entry['genre'].split('-')).split(' ')[0]: entry['game_count'] for entry in genres_game_count}
    # Create a dictionary for review counts
    reviews_count = {''.join(entry['genre'].split('-')).split(' ')[0]: entry['review_count'] for entry in genres_reviews_count}
    return games_count, reviews_count


# Function to get top-rated combat-focused games
def top_combat_picks():
    top_games = (
        Game.objects.filter(genre__genre='Combat-Focused Gameplay')
            .annotate(total_rating=Sum('review__rating'),  # Sum of ratings
                      review_count=Count('review'))       # Count of reviews
            .annotate(average_rating=F('total_rating') / F('review_count'),  # Compute average rating
                      short_description=Substr('description', 1, 10))  # Get the first 10 characters of the description
            .order_by('-average_rating')[1:4]
            .values('title', 'average_rating', 'images', 'price', 'parent_asin', 'short_description')  # Include fields
    )
    return top_games


# Function to generate blog post texts using OpenAI's API
def summarize_reviews(games):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional video game blog writer."},
            {
                "role": "user",
                "content": f"""Generate two separate blog post texts (##BLOG1##, ##BLOG2##), 
                each close to but not more than 100 words.
                - {games[0]}
                - {games[1]}
                - {games[2]}
                The first text should explain why people love playing these video games. 
                Highlight each game title using <b> tags in the text.
                The second text should explain why people do not like playing these same games, 
                again highlighting each game title using <b> tags."""
            }
        ]
    )
    # Parse the API response into two separate blog posts
    blogs = completion.choices[0].message.content.split("##BLOG2##")
    blog1 = blogs[0].replace("##BLOG1##", "").strip()
    blog2 = blogs[1].strip()
    # Return the summarized text as a tuple
    summarized_text = (blog1, blog2)
    return summarized_text