from typing import List, Optional

from pydantic import BaseModel


class Movie(BaseModel):
    adult: bool
    backdrop_path: Optional[str]
    genre_ids: List[int]
    id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str
    title: str
    video: bool
    vote_average: float
    vote_count: int


class Result(BaseModel):
    page: int
    results: List[Movie]
    total_pages: int
    total_results: int
