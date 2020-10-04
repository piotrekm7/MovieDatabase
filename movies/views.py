from dataclasses import asdict

from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from . import omdbapi
from . import models


@login_required
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


class Favorites(LoginRequiredMixin, generic.ListView):
    model = models.Movie
    template_name = 'favorites.html'
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        return models.Movie.objects.filter(favorite__user=self.request.user)


@login_required
def add_to_favorites(request, imdbID: str):
    movie_query = models.Movie.objects.filter(imdbID=imdbID)
    if movie_query.exists():
        movie_db = movie_query.first()
    else:
        movie = omdbapi.get_movie(imdbID)
        movie_db = models.Movie.objects.create(**asdict(movie))

    favorite = models.Favorite.objects.filter(user=request.user, movie=movie_db)
    if not favorite.exists():
        models.Favorite.objects.create(user=request.user, movie=movie_db)

    return redirect('/favorites')


@login_required
def remove_from_favorites(request, imdbID: str):
    models.Favorite.objects.filter(user=request.user, movie__imdbID=imdbID).delete()
    return redirect('/favorites')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, f"Error: {form.errors.as_data()}")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, f"Error: {form.errors.as_data()}")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login')
