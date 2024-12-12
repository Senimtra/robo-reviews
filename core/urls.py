from django.urls import path

from . import views

urlpatterns = [
    # Home view
    path('', views.index, name = 'index'),
    # Get example reviews
    path('review/', views.review, name = 'review'),
    # Sentiment classification
    path('predict/', views.predict, name = 'predict'),
    # Sentiment classification
    path('summarization/', views.summarization, name = 'summarization'),
    ]
