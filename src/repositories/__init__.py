from abc import ABC, abstractmethod


class ApiMovieRepository(ABC):

    @abstractmethod
    async def get_movies_by_query(self, query: str):
        pass
