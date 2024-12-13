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
    # Annotate games with their average rating, order by rating in descending order, and fetch the top 350
    top_games = Game.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating').values('images')[:350]
    # Specific indices of games to select covers for
    top_game_covers_1 = [0, 2, 3, 4, 5, 8, 9, 10, 13, 14, 18, 19, 22, 
                         23, 27, 28, 33, 37, 39, 41, 46, 47, 49, 54]
    top_game_covers_2 = [60, 61, 64, 69, 73, 77, 78, 84, 90, 92, 94, 95, 
                         96, 97, 98, 102, 103, 104, 109, 115, 117, 122, 126, 150]
    top_game_covers_3 = [151, 152, 161, 163, 175, 176, 181, 183, 189, 205, 207, 261,
                         265, 268, 271, 273, 274, 275, 290, 298, 301, 315, 333, 345]
    # Filter the games based on the predefined indices
    top_games_1 = [game['images'] for i, game in enumerate(top_games) if i in top_game_covers_1]
    top_games_2 = [game['images'] for i, game in enumerate(top_games) if i in top_game_covers_2]
    top_games_3 = [game['images'] for i, game in enumerate(top_games) if i in top_game_covers_3]
    return top_games_1, top_games_2, top_games_3


# Function to count games and reviews by genre
def count_ratings_games():
    # Annotate genres with the count of games
    genres_game_count = Genre.objects.values('genre').annotate(game_count=Count('game'))
    # Annotate genres with the count of reviews
    genres_reviews_count = Genre.objects.values('genre').annotate(review_count=Count('game__review'))
    # Create a dictionary for games count
    games_count = {genre['genre']: genre['game_count'] for genre in genres_game_count}
    # Create a dictionary for reviews count
    reviews_count = {genre['genre']: genre['review_count'] for genre in genres_reviews_count}
    # Index view game topic order
    topic_order = ['Combat-Focused Gameplay', 'Engaging Simulated Worlds', 'Action and Tactical Strategy', 'Open Worlds and Discovery']
    # Set up game/review count tuple
    games_and_reviews_count = [(games_count[topic], reviews_count[topic]) for topic in topic_order]
    return games_and_reviews_count


# Function to get top-rated combat-focused games
def top_combat_picks():
    top_games = (
        Game.objects.filter(genre__genre='Combat-Focused Gameplay')
            .annotate(total_rating=Sum('review__rating'),  # Sum of ratings
                      review_count=Count('review'))       # Count of reviews
            .annotate(average_rating=F('total_rating') / F('review_count'),  # Compute average rating
                      short_description=Substr('description', 1, 10))  # Get the first 10 characters of the description
            .order_by('-average_rating')[:30]
            .values('title', 'average_rating', 'images', 'price', 'parent_asin', 'short_description')  # Include fields
    )
    # Select specific top games by predefined indices
    top_games_list = [(game['title'], game['images'], game['price'], game['parent_asin'], game['average_rating'], 
                       game['short_description']) for i, game in enumerate(top_games) if i in [1, 2, 3]]
    return top_games_list


# Function to get top-rated simulation-focused games
def top_sim_picks():
    top_games = (
        Game.objects.filter(genre__genre='Engaging Simulated Worlds')
            .annotate(total_rating=Sum('review__rating'),  # Sum of ratings
                      review_count=Count('review'))       # Count of reviews
            .annotate(average_rating=F('total_rating') / F('review_count'),  # Compute average rating
                      short_description=Substr('description', 1, 10))  # Get the first 10 characters of the description
            .order_by('-average_rating')[:30]
            .values('title', 'average_rating', 'images', 'price', 'parent_asin', 'short_description')  # Include fields
    )
    # Select specific top games by predefined indices
    top_games_list = [(game['title'], game['images'], game['price'], game['parent_asin'], game['average_rating'], 
                       game['short_description']) for i, game in enumerate(top_games) if i in [5, 6, 7]]
    return top_games_list


# Function to get top-rated action and tactical strategy games
def top_tact_picks():
    top_games = (
        Game.objects.filter(genre__genre='Action and Tactical Strategy')
            .annotate(total_rating=Sum('review__rating'),  # Sum of ratings
                      review_count=Count('review'))       # Count of reviews
            .annotate(average_rating=F('total_rating') / F('review_count'),  # Compute average rating
                      short_description=Substr('description', 1, 10))  # Get the first 10 characters of the description
            .order_by('-average_rating')[:30]
            .values('title', 'average_rating', 'images', 'price', 'parent_asin', 'short_description')  # Include fields
    )
    # Select specific top games by predefined indices
    top_games_list = [(game['title'], game['images'], game['price'], game['parent_asin'], game['average_rating'], 
                       game['short_description']) for i, game in enumerate(top_games) if i in [1, 6, 16]]
    return top_games_list


# Function to get top-rated open worlds and discovery games
def top_disco_picks():
    top_games = (
        Game.objects.filter(genre__genre='Action and Tactical Strategy')
            .annotate(total_rating=Sum('review__rating'),  # Sum of ratings
                      review_count=Count('review'))       # Count of reviews
            .annotate(average_rating=F('total_rating') / F('review_count'),  # Compute average rating
                      short_description=Substr('description', 1, 10))  # Get the first 10 characters of the description
            .order_by('-average_rating')[:30]
            .values('title', 'average_rating', 'images', 'price', 'parent_asin', 'short_description')  # Include fields
    )
    # Select specific top games by predefined indices
    top_games_list = [(game['title'], game['images'], game['price'], game['parent_asin'], game['average_rating'], 
                       game['short_description']) for i, game in enumerate(top_games) if i in [20, 24, 25]]
    return top_games_list


# Function to generate example reviews for sentiment analysis
def get_example_review(sentiment):
    """
    Generates a (positive/neutral/negative) review
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a video game enthusiast."},
            {
                "role": "user",
                "content": (
                    f"Generate a short video game review. "
                    f"Make very sure that its sentiment is clearly: {sentiment}."
                    f"It can be any length but not more than 30 words. "
                )
            }
        ]
    )
    # Extract and return the generated review
    example_review = completion.choices[0].message.content
    return example_review


# Function to generate pro/contra blog post texts
def summarize_reviews(games):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional video game blog writer."},
            {
                "role": "user",
                "content": (
                    "Generate two separate blog post texts (##BLOG1##, ##BLOG2##), "
                    "each close to but not more than 100 words. Make sure that the following "
                    "games are mentioned in every text only once:\n"
                    f"- {games[0]}\n"
                    f"- {games[1]}\n"
                    f"- {games[2]}\n"
                    "The first text should explain why people love playing these video games. "
                    "Highlight each game title using <b> tags in the text.\n"
                    "The second text should explain why people do not like playing these same games, "
                    "again highlighting each game title using <b> tags."
                )
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
