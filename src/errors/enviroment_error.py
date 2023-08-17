from fastapi import HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.config.logger import logger


class EnviromentsError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error in the enviroment."


async def exception_enviroment_error(_: Request, exception: EnviromentsError):
    logger.error(exception)
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.detail}
    )
