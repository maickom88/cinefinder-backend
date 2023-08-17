from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette_context import plugins
from starlette_context.middleware import ContextMiddleware

from src.errors.base_error_app import ApiBaseException, exception_base_error

from src.errors.enviroment_error import EnviromentsError, exception_enviroment_error
from src.errors.not_authorized_error import UnauthorizedError, exception_unauthorized_error
from src.errors.not_found_error import NotFoundError, exception_not_found_error
from src.routers.routers import get_routers


def init_app():
    app = _init_fastapi_app()
    return app


def _init_fastapi_app() -> FastAPI:
    app = FastAPI(
        **_get_app_args()
    )
    app = _config_app_middlewares(app)
    app = _config_app_routers(app)
    app = _config_app_exceptions(app)
    return app


def _get_app_args() -> dict:
    args = dict(
        title='CineFinder',
        description='@ CineFinder API',
        version='1.0.0',
        redoc_url=None
    )
    return args


def _config_app_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
            plugins.ForwardedForPlugin(),
        )
    )
    return app


def _config_app_routers(app):
    routers = get_routers()
    routers.sort(key=lambda r: r.get("prefix"))
    [app.include_router(**r) for r in routers]
    return app


def _config_app_exceptions(app):
    app.add_exception_handler(ApiBaseException, exception_base_error)
    app.add_exception_handler(EnviromentsError, exception_enviroment_error)
    app.add_exception_handler(NotFoundError, exception_not_found_error)
    app.add_exception_handler(UnauthorizedError, exception_unauthorized_error)
    return app
