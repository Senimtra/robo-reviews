from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Review


# def detail(request, game_id):
#     game = get_object_or_404(Game, pk=game_id)
#     return render(request, "detail.html", {"game": game})


def index(request):
    latest_reviews_list = Review.objects.order_by("-timestamp")[:5]
    context = {"latest_reviews_list": latest_reviews_list}
    return render(request, "index.html", context)

def detail(request, parent_asin):
    return HttpResponse("You're looking at game %s." % parent_asin)

def reviews(request, parent_asin):
    response = "You're looking at the reviews for game %s."
    return HttpResponse(response % parent_asin)

def genre(request, parent_asin):
    return HttpResponse("You're looking at the genre of game %s." % parent_asin)
