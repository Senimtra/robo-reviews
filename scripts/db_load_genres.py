import os
import csv
import django
import sys

# Add the project directory to the python path
sys.path.append('/home/senimtra/Desktop/SENIMTRA/ROBO-reviews')

# Set up django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_RoboReviews.settings')

django.setup()

from django.db import connection
from core.models import Genre, Game

csv_file_path = '../data/meta_clustered.csv'

# Reset 'id' counter and clear genre table
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM core_genre;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'core_genre';")  # id reset

print('Genre table cleared and ID counter reset.')

# Insert data using bulk_create
with open(csv_file_path, newline = '', encoding = 'utf-8') as file:
    data = csv.DictReader(file)
    objects = []
    for row in data:
        # Fetch the game object for the parent_asin
        game = Game.objects.get(parent_asin = row['parent_asin'])
        # Create a genre object
        genre = Genre(
            game = game,
            genre = row.get('topic', ''),
            )
        # Add genre object to bulk list
        objects.append(genre)
    # Insert genre bulk list
    Genre.objects.bulk_create(objects)

print(f'Finished inserting rows into the Genre table.')
