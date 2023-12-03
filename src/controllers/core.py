from fastapi import Response
from loguru import logger

from ..common.responses import JSONResponseOK
from ..models.core import Query
from ..services import core as service


async def chat(body: Query) -> Response:
    """
    Text report agent controller. This controller is responsible for handling
    requests to the /agents/text route.

    :param body: CompanyQuery object
    :returns: JSONResponseOK object for successful requests
    """
    logger.debug("Entering route at /agents/text...")
    answer = await service.chat(body)
    return JSONResponseOK({"answer": answer})
