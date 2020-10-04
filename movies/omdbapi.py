from typing import List
from dataclasses import dataclass
import inspect

import requests

apikey = 'b82e5b2b'
base_url = f'http://www.omdbapi.com/?apikey={apikey}'


@dataclass
class Movie:
    Title: str
    Year: str
    imdbID: str
    Type: str
    Poster: str


@dataclass
class MovieDetails(Movie):
    Plot: str
    Director: str

    @classmethod
    def from_dict(cls, json):
        return cls(**{
            k: v for k, v in json.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class SearchResults:
    Search: List[Movie]
    totalResults: int
    Response: bool
    pages: int

    def __init__(self, **kwargs):
        self.Response = kwargs['Response'] == 'True'
        if self.Response:
            self.Search = [Movie(**m) for m in kwargs['Search']]
            self.totalResults = int(kwargs['totalResults'])
            self.pages = (self.totalResults - 1) // 10 + 1


def search_movies(title: str = "", page: int = 1):
    url = f'{base_url}&s={title}&page={page}'
    response = requests.get(url)
    return SearchResults(**response.json())


def get_movie(imdbID: str):
    url = f'{base_url}&i={imdbID}'
    response = requests.get(url)
    return MovieDetails.from_dict(response.json())
