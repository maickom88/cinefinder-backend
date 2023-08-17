from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.config.logger import logger


class NotFoundError(Exception):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Error not found while accessing this route."


async def exception_not_found_error(_: Request, exception: NotFoundError):
    logger.error(exception)
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.detail}
    )
