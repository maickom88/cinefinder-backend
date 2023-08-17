from typing import List

from fastapi import APIRouter

from src.config.logger import logger
from src.models.movies_model import Movie
from src.repositories.tmdb_repository import TMDBRepository
from src.services.movies_services.movie_service import MovieService

router = APIRouter()
repository_movie = TMDBRepository()

movie_router = {
    "router": router,
    "prefix": "/movie",
    "tags": ["Movie"],
}


@router.get(path="", response_model=List[Movie])
def get_movies(name: str):
    logger.info("Starting request to movie_controller.get_movie_by_query")
    service = MovieService(repository=repository_movie)
    return service.get_movies_by_query(name_movie=name)
