from django.db import models
from django.contrib.auth import get_user_model


class Movie(models.Model):
    """DB model for storing movie info."""
    imdbID = models.CharField(max_length=255, primary_key=True)
    Title = models.CharField(max_length=255)
    Year = models.CharField(max_length=255)
    Type = models.CharField(max_length=255)
    Poster = models.URLField()
    Plot = models.TextField()
    Director = models.CharField(max_length=255)


class Favorite(models.Model):
    """Managing favorite movies."""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
