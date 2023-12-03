from fastapi import Request
from fastapi.exceptions import RequestValidationError

from .exceptions import BodyException


async def validation_exception_handler(
    req: Request, exc: RequestValidationError
) -> BodyException:
    """
    Handler for RequestValidationError. This handler is used to enforce the
    structure of the error response. Intended to replace FastAPI's default
    RequestValidationError with our custom BodyException.

    :param req: Request object
    :param exc: RequestValidationError object
    :returns: BodyException object
    """
    # reformat exception to match our error response format
    raise BodyException(exc)
