from django.contrib import admin

from .models import Movie, Favorite

admin.site.register(Movie)
admin.site.register(Favorite)
