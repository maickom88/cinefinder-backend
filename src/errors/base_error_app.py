from fastapi import HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.config.logger import logger


class ApiBaseException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Error in the server while accessing this route."


async def exception_base_error(_: Request, exception: ApiBaseException):
    logger.error(exception)
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.detail}
    )
