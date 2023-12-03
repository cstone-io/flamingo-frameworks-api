import logging
from typing import Callable

from fastapi import Request, Response, HTTPException

from .exceptions import ServerException


async def catch_exceptions_middleware(
    request: Request, call_next: Callable
) -> Response:
    """
    Middleware designed to catch all unhandled exceptions and return a server
    error response. This is primarily made to be used when testing locally in
    place of the Sentry middleware.

    :param request: The request object
    :param call_next: The next middleware in the chain
    :return: The response object
    """
    try:
        return await call_next(request)
    except HTTPException as e:  # FastAPI HTTPException are expected behavior
        raise e
    except Exception as e:
        logging.exception(e)
        raise ServerException("Internal Server Error")
