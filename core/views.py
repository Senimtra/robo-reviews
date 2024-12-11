from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Import functions to handle business logic
from .functions import top_games_images, count_ratings_games, top_combat_picks, top_sim_picks
from .functions import top_tact_picks, top_disco_picks, get_example_review, summarize_reviews
from .models import Review

import requests
import json


# Main index view to display game-related information
def index(request):

    # Fetch top combat game picks for display
    top_combat_game_picks = top_combat_picks()
    # Fetch top simulation game picks for display
    top_sim_game_picks = top_sim_picks()
    # Fetch top action and tactical strategy games
    top_tact_game_picks = top_tact_picks()
    # Fetch top open worlds and discovery games
    top_disco_game_picks = top_disco_picks()
    # Set up top pick game details
    top_pick_games = [top_combat_game_picks, top_sim_game_picks, 
                      top_tact_game_picks, top_disco_game_picks]

    # Extract the titles of the top combat games for summarization
    # summ_games = [game['title'] for game in top_combat_game_picks]
    # Generate blog-style summaries for the top games
    # summarized_text = summarize_reviews(summ_games)
    # # Fetch the list of images for the top-rated games
    top_games_image_list = top_games_images()
    # Fetch game and review counts categorized by genre
    genre_ratings_games = count_ratings_games()

    # Set up game cluster section list
    section_list = ['Combat-Focused Gameplay', 'Engaging Simulated Worlds', 
                    'Action and Tactical Strategy', 'Open Worlds and Discovery']
    section_descr = ["""Represents games centered on battles, warfare, and multiplayer 
                     combat.<br />Includes FPS, tactical shooters, and MOBAs, 
                     with a focus on defeating enemies and teamwork.""",
                     """Encompasses games involving sports, racing, and team challenges,<br />
                     as well as simulation games like life management or vehicle-based gameplay.""", 
                     """Covers games with action-packed combat, exploration, and abilities,<br />
                     while also including strategic games where planning and tactical 
                     execution are essential.""",
                     """Reflects games with a focus on story-driven adventures,<br />open-world 
                     exploration, life simulation, survival, or sandbox-style gameplay."""]
    section_descr_long = ["""<h4><b>Unleash Your Inner Warrior</b></h4><div>Step into the 
                          intense world of battle-centric games, where strategy, teamwork, 
                          and quick reflexes lead to victory.<br />From fast-paced FPS titles 
                          like Call of Duty to strategic MOBAs like League of Legends, these 
                          games focus on defeating enemies, mastering tactics, and working with 
                          your team to dominate the battlefield.<br />Ready to prove your skills? 
                          The fight begins now!</div>""", 
                          """<h4><b>Immerse Yourself in Simulated Realities</b></h4><div>Step into 
                          simulated worlds where your choices shape the experience.<br />Whether racing 
                          at high speeds, managing life in The Sims,<br />or teaming up in competitive sports, 
                          these games offer rich and engaging gameplay. From realistic simulations 
                          to strategic competitions,<br />test your skills and creativity.<br /> 
                          Ready to begin your simulation journey? Dive in today!</div>""", 
                          """<h4><b>Thrilling Action Meets Tactical Brilliance</b></h4><div>Experience 
                          a thrilling mix of action and strategy. Battle through intense combat, 
                          explore immersive worlds, and conquer challenges with unique abilities.<br />
                          From fast-paced action to tactical planning, these games test your skills. 
                          Master strategy and lead your team to victory. Ready for the challenge? 
                          The adventure begins now!</div>""", 
                          """<h4><b>Embark on Epic Journeys of Exploration</b></h4><div>Set off on 
                          unforgettable adventures in vast open worlds full of discovery. 
                          These games feature rich narratives, immersive characters, and expansive 
                          landscapes, from lush forests to survival environments.<br />Whether 
                          crafting your destiny, facing challenges, or building unique creations, 
                          the open-world genre invites you to explore, create, and shape your experience. 
                          Ready to begin? The adventure awaits!</div>"""]
    section_count = [1, 2, 3, 4]
    game_sections = zip(section_list, section_descr, section_count, section_descr_long, 
                        genre_ratings_games, top_pick_games)
    
    # Prepare context data to send to the template
    context = {
        'game_sections': game_sections,
        'top_games_image_list': top_games_image_list,  # List of images for the top games     
        # 'summarized_text': summarized_text  # Summarized blog content
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
            print(external_response)
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
