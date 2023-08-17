from src.repositories import ApiMovieRepository


class MovieService:
    def __init__(self, repository: ApiMovieRepository):
        self.repository = repository

    def get_movies_by_query(self, name_movie: str):
        return self.repository.get_movies_by_query(name_movie)
