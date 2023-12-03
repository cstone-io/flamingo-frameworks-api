from fastapi import status
from fastapi.responses import JSONResponse, PlainTextResponse


class JSONResponseOK(JSONResponse):
    """
    Shorthand for a JSONResponse with a 200 status code.
    """

    def __init__(self, content: dict, headers=None, **kwargs) -> None:
        """
        :param content: JSON serializable content (as a positional arg)
        :param headers: Optional headers
        :param kwargs: Optional additional arguments
        """
        super().__init__(
            status_code=status.HTTP_200_OK, content=content, headers=headers, **kwargs
        )


class PlainTextResponseOK(PlainTextResponse):
    """
    Shorthand for a PlainTextResponse with a 200 status code.
    """

    def __init__(self, content: str, headers=None, **kwargs) -> None:
        """
        :param content: Plain text content (as a positional arg)
        :param headers: Optional headers
        :param kwargs: Optional additional arguments
        """
        super().__init__(
            status_code=status.HTTP_200_OK,
            content=content,
            headers=headers,
            media_type="text/plain",
            **kwargs,
        )
