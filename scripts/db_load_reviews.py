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
from core.models import Review, Game

csv_file_path = '../data/reviews_cleaned.csv'

# Reset 'id' counter and clear review table
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM core_review;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'core_review';")  # id reset

print('Review table cleared and ID counter reset.')

# Insert data using bulk_create
with open(csv_file_path, newline = '', encoding = 'utf-8') as file:
    data = csv.DictReader(file)
    objects = []
    for row in data:
        # Fetch the game object for the parent_asin
        game = Game.objects.get(parent_asin = row['parent_asin'])
        # Create a review object
        review = Review(
            game = game,
            rating = int(row.get('rating', 0)),
            title = row.get('title', ''),
            text = row.get('text', ''),
            user_id = row.get('user_id', ''),
            timestamp = row.get('timestamp', '2023-01-01T00:00:00'),
            helpful_vote = int(row.get('helpful_vote', 0)),
            verified_purchase = row.get('verified_purchase', '').lower() == 'true',
            )
        # Add review object to bulk list
        objects.append(review)
    # Insert review bulk list
    Review.objects.bulk_create(objects)

print(f'Finished inserting rows into the Review table.')
