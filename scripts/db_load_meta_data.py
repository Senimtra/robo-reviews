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
from core.models import Game

csv_file_path = '../data/meta_cleaned.csv'

# Reset 'id' counter and clear review table
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM core_game;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'core_game';")  # id reset

print('Game table cleared and ID counter reset.')

# Insert data using bulk_create
with open(csv_file_path, newline = '', encoding = 'utf-8') as file:
    data = csv.DictReader(file)
    objects = []
    for row in data:
        # Create a game object
        game = Game(
            parent_asin = row['parent_asin'],
            title = row.get('title', ''),
            features = row.get('features', None),
            description = row.get('description', None),
            price = float(row.get('price', 0)) if row.get('price') else None,
            images = row.get('images', None),
            store = row.get('store', None),
            categories = row.get('categories', None),
            details = row.get('details', None),
            category = row.get('category', None),
        )
        # Add game object to bulk list
        objects.append(game)
    # Insert game bulk list
    Game.objects.bulk_create(objects)

print(f'Finished inserting rows into the Game table.')
