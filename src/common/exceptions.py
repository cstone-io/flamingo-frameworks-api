from typing import List, Optional

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """
    Data model to enforce the structure of the error response. Param and
    location are optional because they are not always present in the error.
    """

    value: str
    msg: str
    param: Optional[str] = None
    location: Optional[str] = None


class CustomHTTPException(HTTPException):
    """
    Core exception class for all custom exceptions. This class is used to
    enforce the structure of the error response.
    """

    def __init__(
        self, status_code: int, errors: List[ErrorDetail], headers: dict = None
    ) -> None:
        """
        :param status_code: HTTP status code
        :param errors: List of ErrorDetail objects
        :param headers: Optional HTTP headers
        """
        detail = {"errors": [error.dict() for error in errors]}

        if headers is None:
            headers = {}
        headers.setdefault("Content-Type", "application/json")

        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AuthException(CustomHTTPException):
    """
    Exception class for authentication errors. This class is used to enforce
    the structure of the error response. Simplified shortcut allows for proper
    output while only taking a string as input.
    """

    def __init__(self, token: str, msg: str) -> None:
        """
        :param token: Invalid token
        :param msg: Error message
        """
        error = ErrorDetail(
            value=token,
            msg=msg,
            param="Authorization",
            location="header",
        )
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            errors=[error],
        )


class BodyException(CustomHTTPException):
    """
    Exception class for body errors. This class is used to enforce the
    structure of the error response. Intended to replace ValidationException
    class called by FastAPI when parsing the request body.
    """

    def __init__(self, exception: RequestValidationError) -> None:
        """
        :param exception: RequestValidationError object
        """
        details = exception.errors()
        errors = []
        for error in details:
            param = error.get("loc")[1] if len(error.get("loc", [])) > 1 else "invalid"
            errors.append(
                ErrorDetail(
                    value=exception.body.get(param)
                    if hasattr(exception, "body") and isinstance(exception.body, dict)
                    else "could not parse body",
                    msg=error.get("msg"),
                    param=param,
                    location="body",
                )
            )
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=errors,
        )


class ServerException(CustomHTTPException):
    """
    Exception class for server errors. This class is used to enforce the
    structure of the error response. Simplified shortcut allows for proper
    output while only taking a string as input. Intended to be used in
    conjunction with middlware to catch all unhandled exceptions.
    """

    def __init__(self, msg: str) -> None:
        """
        :param msg: Error message
        """
        error = ErrorDetail(
            value="Server error",
            msg=msg,
        )
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errors=[error],
        )
