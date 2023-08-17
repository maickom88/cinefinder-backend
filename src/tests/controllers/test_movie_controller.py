from http.client import HTTPException
from typing import List

import pydantic
import pytest
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from src.config.config_app import init_app
from src.errors.base_error_app import ApiBaseException
from src.errors.not_found_error import NotFoundError
from src.models.movies_model import Movie
from src.services.movies_services.movie_service import MovieService

client = TestClient(init_app())


def test_for_root_application():
    response = client.get("/")
    assert response.status_code == 404


def test_should_list_movies_for_name(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(MovieService, "get_movies_by_query", sucess_request)
    params = {"name": "rambo"}
    response = client.get("/movie", params=params)
    assert bool(response.json())
    assert response.status_code == 200


def test_should_list_empty(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(MovieService, "get_movies_by_query", empty_list)
    params = {"name": ""}
    response = client.get("/movie", params=params)
    results = pydantic.parse_obj_as(List[Movie], response.json())
    assert len(results) == 0
    assert response.status_code == 200


def test_should_failure_422_error(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(MovieService, "get_movies_by_query", replace_only_error)
    response = client.get("/movie")
    assert response.status_code == 422


def test_should_failure_404_error(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(MovieService, "get_movies_by_query", replace_error_not_found)
    params = {"name": ""}
    response = client.get("/movie", params=params)
    assert response.status_code == 404


def test_should_failure_500_error(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(MovieService, "get_movies_by_query", replace_error_unexpected)
    params = {"name": ""}
    response = client.get("/movie", params=params)
    assert response.status_code == 500


def replace_only_error():
    raise Exception


def replace_error_not_found(*_, **__):
    raise NotFoundError()


def replace_error_unexpected(*_, **__):
    raise ApiBaseException()


def empty_list(*_, **__):
    return JSONResponse(
        status_code=200,
        content=[]
    )


def sucess_request(*_, **__):
    return JSONResponse(
        status_code=200,
        content=''' 
         {
      "adult": false,
      "backdrop_path": "/7drO1kYgQ0PnnU87sAnBEphYrSM.jpg",
      "genre_ids": [
        16,
        28,
        27
      ],
      "id": 1083862,
      "original_language": "ja",
      "original_title": "バイオハザード：デスアイランド",
      "overview": "In San Francisco, Jill Valentine is dealing with a zombie outbreak and a new T-Virus, Leon Kennedy is on the trail of a kidnapped DARPA scientist, and Claire Redfield is investigating a monstrous fish that is killing whales in the bay. Joined by Chris Redfield and Rebecca Chambers, they discover the trail of clues from their separate cases all converge on the same location, Alcatraz Island, where a new evil has taken residence and awaits their arrival.",
      "popularity": 912.474,
      "poster_path": "/xzAQ28moSPEZxOHJ7WL1mX6hb5H.jpg",
      "release_date": "2023-06-22",
      "title": "Resident Evil: Death Island",
      "video": false,
      "vote_average": 7.708,
      "vote_count": 542
    }
        '''
    )
