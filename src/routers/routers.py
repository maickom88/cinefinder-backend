from src.controllers.movie_controller import movie_router


def get_routers() -> list:
    return [
        movie_router,
    ]
