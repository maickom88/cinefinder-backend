from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.config.logger import logger


class UnauthorizedError(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Error Unauthorized while accessing this route."


async def exception_unauthorized_error(_: Request, exception: UnauthorizedError):
    logger.error(exception)
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.detail}
    )
