from django.db import models

# Create table: game meta data
class Game(models.Model):
    parent_asin = models.CharField(max_length = 20, unique = True)
    title = models.CharField(max_length = 255)
    features = models.TextField(null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    images = models.URLField(max_length = 500, null = True, blank = True)
    store = models.CharField(max_length = 255, null = True, blank = True)
    categories = models.TextField(null = True, blank = True)
    details = models.TextField(null = True, blank = True)
    category = models.CharField(max_length = 255, null = True, blank = True)

    def __str__(self):
        return self.title

# Create table: reviews
class Review(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete = models.CASCADE,
        to_field = 'parent_asin',
        db_column = 'parent_asin',
    )
    rating = models.IntegerField()
    title = models.CharField(max_length = 255)
    text = models.TextField()
    user_id = models.CharField(max_length = 255)
    timestamp = models.DateTimeField()
    helpful_vote = models.IntegerField(null = True, blank = True)
    verified_purchase = models.BooleanField(default = False)

    def __str__(self):
        return f"Review for {self.game.title} by {self.user_id}"
