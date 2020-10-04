from typing import List
from dataclasses import dataclass

import requests


@dataclass
class Movie:
    Title: str
    Year: str
    imdbID: str
    Type: str
    Poster: str


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
            self.pages = (self.totalResults-1)//10 + 1


def search_movies(title: str = "", page: int = 1):
    apikey = 'b82e5b2b'
    url = f'http://www.omdbapi.com/?apikey={apikey}&s={title}&page={page}'
    response = requests.get(url)
    return SearchResults(**response.json())
