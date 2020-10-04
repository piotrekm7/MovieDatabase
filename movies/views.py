from dataclasses import asdict

from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from . import omdbapi
from . import models


def search_movies(request):
    title = request.GET.get('title', default='')
    page = int(request.GET.get('page', default=1))
    search_result = omdbapi.search_movies(title, page)
    context = {
        'search_phrase': title,
        'result': search_result.Response,
    }
    if search_result.Response:
        context.update({
            'search_phrase': title,
            'page': page,
            'next_page': page + 1 if page < search_result.pages else page,
            'previous_page': page - 1 if page > 1 else page,
            'result': search_result.Response,
            'movies': search_result.Search
        })

    return render(request, 'search.html', context=context)


class Favorites(generic.ListView):
    model = models.Movie
    template_name = 'favorites.html'
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        user = get_user_model().objects.filter(username='piotr').first()
        return models.Movie.objects.filter(favorite__user=user)


def add_to_favorites(request, imdbID: str):
    movie_query = models.Movie.objects.filter(imdbID=imdbID)
    if movie_query.exists():
        movie_db = movie_query.first()
    else:
        movie = omdbapi.get_movie(imdbID)
        movie_db = models.Movie.objects.create(**asdict(movie))

    user = get_user_model().objects.filter(username='piotr').first()

    favorite = models.Favorite.objects.filter(user=user, movie=movie_db)
    if not favorite.exists():
        models.Favorite.objects.create(user=user, movie=movie_db)

    return HttpResponseRedirect('/favorites')


def remove_from_favorites(request, imdbID: str):
    user = get_user_model().objects.filter(username='piotr').first()
    models.Favorite.objects.filter(user=user, movie__imdbID=imdbID).delete()
    return HttpResponseRedirect('/favorites')

