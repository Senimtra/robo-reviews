from django.contrib import admin

from .models import Game, Review, Genre

admin.site.register([Game, Review, Genre])
