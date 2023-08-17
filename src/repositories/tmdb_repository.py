from typing import List

import pydantic
import requests
from src.config.enviroment import env
from src.errors.base_error_app import ApiBaseException
from src.errors.not_authorized_error import UnauthorizedError
from src.errors.not_found_error import NotFoundError
from src.models.movies_model import Result, Movie
from src.repositories import ApiMovieRepository


class TMDBRepository(ApiMovieRepository):
    def __init__(self):
        self.http = requests
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {env.token_tmdb()}"
        }

    def get_movies_by_query(self, query: str) -> List[Movie]:
        params = {
            "query": query,
            "include_adult": False,
            "language": "pt-BR",
            "page": 1,
            "region": "Brazil"
        }
        result = self.http.get(f'{env.api_base_tmdb()}search/movie', headers=self.headers, params=params)
        if result.status_code == 200:
            result_model = pydantic.parse_obj_as(Result, result.json())
            result_with_url_images = list(map(self.__set_images, result_model.results))
            return result_with_url_images
        if result.status_code == 404:
            raise NotFoundError()
        if result.status_code == 401:
            raise UnauthorizedError()
        else:
            raise ApiBaseException()

    @staticmethod
    def __set_images(movie: Movie) -> List[Movie]:
        background = movie.backdrop_path
        poster = movie.poster_path
        movie.backdrop_path = f'https://image.tmdb.org/t/p/w500{background}'
        movie.poster_path = f'https://image.tmdb.org/t/p/w500{poster}'
        return movie
