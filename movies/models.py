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


class FacebookProfileManager(models.Manager):

    def create(self, facebook_id, **kwargs):
        """Creates new user and binds to it facebook profile"""
        password = get_user_model().objects.make_random_password()
        user = get_user_model().objects.create_user(username=facebook_id, password=password)
        facebook_profile = self.model(user=user, facebook_id=facebook_id, **kwargs)
        facebook_profile.save()
        return facebook_profile


class FacebookProfile(models.Model):
    """DB model for storing facebook user info"""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    facebook_id = models.BigIntegerField(unique=True, db_index=True, primary_key=True)

    objects = FacebookProfileManager()
