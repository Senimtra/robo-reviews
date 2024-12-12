from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Import functions to handle business logic
from .functions import top_games_images, count_ratings_games, top_combat_picks, top_sim_picks
from .functions import top_tact_picks, top_disco_picks, get_example_review, summarize_reviews
from .models import Review

import requests
import json


# Fetch top combat game picks
top_combat_game_picks = top_combat_picks()
# Fetch top simulation game picks
top_sim_game_picks = top_sim_picks()
# Fetch top action and tactical strategy games
top_tact_game_picks = top_tact_picks()
# Fetch top open worlds and discovery games
top_disco_game_picks = top_disco_picks()


# Extract the titles of the top games for summarization
summ_combat = [game[0] for game in top_combat_game_picks]
summ_sim = [game[0] for game in top_sim_game_picks]
summ_tact = [game[0] for game in top_tact_game_picks]
summ_disco = [game[0] for game in top_disco_game_picks]

summ_titles = [summ_combat, summ_sim, summ_tact, summ_disco]


# Main index view to display game-related information
def index(request):

    # Set up top pick game details
    top_pick_games = [top_combat_game_picks, top_sim_game_picks, 
                      top_tact_game_picks, top_disco_game_picks]

    # # Fetch the list of images for the top-rated games
    top_games_image_list = top_games_images()
    # Fetch game and review counts categorized by genre
    genre_ratings_games = count_ratings_games()

    # Set up game cluster section entries
    section_list = ['Combat-Focused Gameplay', 'Engaging Simulated Worlds', 
                    'Action and Tactical Strategy', 'Open Worlds and Discovery']
    section_descr = ["""Games featuring FPS, tactical shooters, and MOBAs, 
                     focused on teamwork and combat.""",
                     """Games featuring sports, racing, team challenges, 
                     and life or vehicle-based simulations.""", 
                     """Games featuring action combat, exploration, abilities, 
                     and strategic planning and tactics.""",
                     """Games featuring story-driven adventures, open worlds, 
                     survival, or sandbox gameplay."""]
    section_descr_long = ["""<h4><b>Unleash Your Inner Warrior</b></h4><div>Step into battle-centric 
                          games where strategy, teamwork, and reflexes win. From FPS like Call of Duty 
                          to MOBAs like League of Legends, master tactics and dominate. 
                          Ready to prove your skills? The fight starts now!</div>""", 
                          """<h4><b>Immerse Yourself in Simulated Realities</b></h4><div>Enter simulated 
                          worlds where your choices shape the game. Race at high speeds, manage life in 
                          The Sims, or compete in sports—these games offer creative challenges. 
                          Ready to start your journey? Dive in today!</div>""", 
                          """<h4><b>Thrilling Action Meets Tactical Brilliance</b></h4><div>Experience 
                          action and strategy in intense combat, immersive worlds, and unique abilities. 
                          From fast-paced battles to tactical planning, master strategy and lead your 
                          team to victory. Ready for the challenge? The adventure begins now!</div>""", 
                          """<h4><b>Embark on Epic Journeys of Exploration</b></h4><div>Venture into 
                          vast open worlds filled with discovery, rich narratives, and immersive 
                          characters. Explore lush landscapes, craft your destiny, face challenges, 
                          or build unique creations. Ready to begin? The adventure awaits!</div>"""]
    sentiment_placeholder = """<p><span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;stellar&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 76, 0);">&nbsp;&nbsp;gameplay&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;and&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;capt&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;##ivating&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;story&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;make&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 94, 0);">&nbsp;&nbsp;celestial&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;odyssey&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;a&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;must&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 80, 0);">&nbsp;&nbsp;-&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;play&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;!&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;engaging&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 72, 0);">&nbsp;&nbsp;mechanics&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;and&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;stunning&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;visuals&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;keep&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;you&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;hooked&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;from&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;start&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;to&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;finish&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;.&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 84, 0);">&nbsp;&nbsp;a&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;true&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;gem&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 40, 0);">&nbsp;&nbsp;in&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 67, 0);">&nbsp;&nbsp;gaming&nbsp;&nbsp;</span> <span style="background-color: rgb(0, 100, 0);">&nbsp;&nbsp;!&nbsp;&nbsp;</span></p>"""
    section_count = [1, 2, 3, 4]

    # summarized_text = [summarized_combat, summarized_sim, summarized_tact, summarized_disco]
    
    # Set up game cluster section list
    game_sections = zip(section_list, section_descr, section_count, section_descr_long, 
                        genre_ratings_games, top_pick_games)  #, summarized_text)
    
    # Prepare context data to send to the template
    context = {
        'game_sections': game_sections,
        'top_games_image_list_0': top_games_image_list[0],  # List of images for the top games
        'top_games_image_list_1': top_games_image_list[1],  # List of images for the top games
        'sentiment_placeholder': sentiment_placeholder
    }
    
    # Render the 'index.html' template with the provided context
    return render(request, 'index.html', context)


# Get sentiment prediction
def predict(request):
    if request.method == "POST":
        data = json.loads(request.body)
        review = data.get("review", "")
        external_url = "http://127.0.0.1:5000/predict"
        # POST request
        response = requests.post(
            external_url,
            json={"review": review},
            headers={"Content-Type": "application/json"}
        )
        # Return response from external server
        if response.status_code == 200:
            external_response = response.json()
            return JsonResponse({"success": True, "data": external_response})
        else:
            return JsonResponse(
                {"success": False, "error": "Failed to fetch from external server"},
                status=response.status_code,
            )
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Get example reviews
def review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sentiment = data.get('sentiment', '')
        # Request review from api
        review = get_example_review(sentiment).strip('"')
        context = {'review': review}
    return JsonResponse(context)


# Get summarization texts
def summarization(request):
    if request.method == 'POST':
        topic = json.loads(request.body)['topic']
        summarized_texts = summarize_reviews(summ_titles[topic])
        context = {'summarization': summarized_texts}
    return JsonResponse(context)
