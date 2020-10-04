from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda req: redirect('/search/')),
    path('search/', views.search_movies),
    path('favorites/', views.Favorites.as_view()),
    path('add_to_favorites/<str:imdbID>/', views.add_to_favorites),
    path('remove_from_favorites/<str:imdbID>/', views.remove_from_favorites),
    path('register/', views.register_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view)
]
