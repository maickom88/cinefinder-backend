import os
from dotenv import load_dotenv

from src.config.logger import logger


class Environment:
    def __init__(self):
        load_dotenv()
        self._ENV_API_HOST: str = os.getenv("HOST")
        self._ENV_API_PORT: str = os.getenv("PORT")
        self._ENV_IS_DEBUG: bool = os.getenv("DEBUG")

        self._ENV_TOKEN_TMDB: str = os.getenv("TMDB_TOKEN")
        self._ENV_API_BASE_TMDB: str = os.getenv("TMBD_API_BASE")

    def environment_validate(self) -> None:
        msg = []
        for k in self.__dict__:
            if self.__dict__[k] is None:
                msg.append(f"{k} is not configured in environment")
        if len(msg) > 0:
            logger.error(f"Error in ENV, not configure: {msg}")
            raise EnvironmentError(msg)

    def api_host(self) -> str:
        return self._ENV_API_HOST

    def api_port(self) -> int:
        return int(self._ENV_API_PORT)

    def is_debug(self) -> bool:
        return bool(self._ENV_IS_DEBUG)

    def token_tmdb(self) -> str:
        return self._ENV_TOKEN_TMDB

    def api_base_tmdb(self) -> str:
        return self._ENV_API_BASE_TMDB


env = Environment()
