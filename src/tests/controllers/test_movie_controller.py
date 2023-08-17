from http.client import HTTPException
from typing import List

import pydantic
import pytest
from starlette.testclient import TestClient

from src.config.config_app import init_app
from src.errors.base_error_app import ApiBaseException
from src.errors.not_found_error import NotFoundError
from src.models.movies_model import Movie
from src.services.movies_services.movie_service import MovieService

client = TestClient(init_app())


def mocked_response():
    raise HTTPException(status_code=400, detail='gibberish')


def test_for_root_application():
    response = client.get("/")
    assert response.status_code == 404


def test_should_list_movies_for_name():
    params = {"name": "rambo"}
    response = client.get("/movie", params=params)
    assert bool(response.json())
    assert response.status_code == 200


def test_should_list_empty():
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
