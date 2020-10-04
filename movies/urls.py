from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search_movies),
    path('favorites/', views.Favorites.as_view()),
    path('add_to_favorites/<str:imdbID>/', views.add_to_favorites),
    path('remove_from_favorites/<str:imdbID>/', views.remove_from_favorites)
]
