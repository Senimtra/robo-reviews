from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    # ex: /
    path('<str:parent_asin>/', views.detail, name = 'detail'),
    # ex: /B00XY0IVK4/reviews/
    path('<str:parent_asin>/reviews/', views.reviews, name = 'reviews'),
    # ex: /B00XY0IVK4/genre/
    path('<str:parent_asin>/genre/', views.genre, name = 'genre'),
]
